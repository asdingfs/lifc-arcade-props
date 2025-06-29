import com.heroicrobot.controlsynthesis.*;
import com.heroicrobot.dropbit.discovery.*;
import com.heroicrobot.dropbit.common.*;
import com.heroicrobot.dropbit.registry.*;
import com.heroicrobot.dropbit.devices.*;
import com.heroicrobot.dropbit.devices.pixelpusher.*;
import java.util.*;

class TestObserver implements Observer {
  public boolean hasStrips = false;
  public void update(Observable registry, Object updatedDevice) {
    println("Registry changed!");
    if (updatedDevice != null) {
      println("Device change: " + updatedDevice);
    }
    this.hasStrips = true;
  }
}

// load devices
DeviceRegistry registry;
TestObserver testObserver;
// load data (defaults);
FrameData frameData;
// load fonts
PFont h1Font;
PFont h2Font;
PFont h3Font;
// changed
boolean isChanged = false;

// START: helper methods for rendering
void resetBackground() {
  background(frameData.arcadeBackground);
}
String padZeros(int num, int sf) {
  return String.format("%0" + Integer.toString(sf) + "d", num).replace(' ', '0');
}
// END: of helper methods

void settings() {
  size(FrameData.widthTotal, FrameData.heightTotal);
}

void setup() {
  // initialize fonts
  h1Font = createFont(FrameData.fontName, FrameData.h1FontSizePx);
  h2Font = createFont(FrameData.fontName, FrameData.h2FontSizePx);
  h3Font = createFont(FrameData.fontName, FrameData.h3FontSizePx);

  // create default frame data
  // modify FrameData based on arguments, you can find the variables in FrameData.pde
  ArgumentParser parser = new ArgumentParser(args);
  if (args != null && args.length > 0) {
    println("Processing received arguments: " + Arrays.toString(args));
    frameData = parser.toFrameData();
  } else {
    println("No arguments received, using default values.");
    FrameDataBuilder builder = new FrameDataBuilder();
    frameData = builder.build();
  }
  isChanged = true; // set changed to true, so we can render frame data
  // check if we're to save preview only, or to render frame data continuously
  if (parser.toSavePreview()) {
    println("Saving preview and exiting...");
    preview(frameData);
    save(parser.getSavePreviewLocation());
    exit();
  } else {
    println("Rendering frame data...");
    // initialize registry
    registry = new DeviceRegistry();
    testObserver = new TestObserver();
    registry.addObserver(testObserver);
    // render frame data
    background(0);
    resetBackground();
    renderFrameData(frameData);
  }
}

void draw() {
  if (testObserver.hasStrips) {
    if (isChanged) {
      loadPixels();
      registry.startPushing();
      List<Strip> strips = registry.getStrips();
      // iterate through each available strips, and sample pixels
      int y = 0;
      int scaleY = height / (strips.size());
      for (Strip strip: strips) {
        int scaleX = width / strip.getLength();
        for (int x = 0; x < strip.getLength(); x++) {
          color c = pixels[y*scaleY*width+x*scaleX];
          // color c = get(x*scaleX, y*scaleY); // this is a slower, but what was written in docs
          strip.setPixel(c, x);
        }
        y++;
      }
      isChanged = false;
      delay(100); // wait a bit, so we can see the data
    } else {
      // clean up registry, so there's no updating (hence no flickering)
      delay(100);
      registry.stopPushing();
    }
  }
}


void renderStringRow(String str, int x, int y, color colour) {
  textAlign(CENTER);
  rectMode(CENTER);
  fill(colour);
  text(str, x, y);
}

void renderFrameData(FrameData dt) {
  // set modes
  rectMode(CENTER);
  imageMode(CENTER);

  // load images
  PImage p1Img = loadImage(dt.p1ImgSrc);
  PImage p2Img = loadImage(dt.p2ImgSrc);

  // resize & fill image to container & render p1 & p2 images
  int imgSize = (int) Math.floor(FrameData.imgContainerSizePx * FrameData.imgDpSize * FrameData.imgScale);
  SquareFill p1ImgDim = new SquareFill(p1Img.width, p1Img.height, imgSize);
  p1Img.resize(p1ImgDim.w, p1ImgDim.h); // order is important
  SquareCrop p1ImgCrop = new SquareCrop(p1Img.width, p1Img.height, imgSize);
  p1Img = p1Img.get(p1ImgCrop.x, p1ImgCrop.y, p1ImgCrop.w, p1ImgCrop.h);
  image(p1Img, dt.widthCenter - (2 * FrameData.ledPanelWidth * FrameData.imgDpSize), dt.heightCenter);
  SquareFill p2ImgDim = new SquareFill(p2Img.width, p2Img.height, imgSize);
  p2Img.resize(p2ImgDim.w, p2ImgDim.h); // order is important
  SquareCrop p2ImgCrop = new SquareCrop(p2Img.width, p2Img.height, imgSize);
  p2Img = p2Img.get(p2ImgCrop.x, p2ImgCrop.y, p2ImgCrop.w, p2ImgCrop.h);
  image(p2Img, dt.widthCenter + (2 * FrameData.ledPanelWidth * FrameData.imgDpSize), dt.heightCenter);

  // render title row
  textFont(h1Font);
  fill(255);
  renderStringRow("LIFC 2025: RETRO ARCADE", dt.widthCenter, 50, dt.arcadeMagenta);

  // render top score row
  int centerX = dt.widthCenter;
  fill(dt.arcadeRed);
  rect(centerX, 86, 128, 40, 32);
  textFont(h2Font);
  renderStringRow("TOP", centerX, 100, color(255));
  renderStringRow(padZeros(dt.topScore, 7), centerX, 140, dt.arcadeWhite);

  // render p1 & p2 player score rows
  int middleOffsetX = -4;
  int leftX = centerX - (FrameData.ledPanelWidth + middleOffsetX) * FrameData.imgDpSize + 40;
  int rightX = centerX + (FrameData.ledPanelWidth + middleOffsetX) * FrameData.imgDpSize - 40;
  renderStringRow("1UP", leftX, 160, dt.arcadeCyan);
  renderStringRow(padZeros(dt.p1Score, 7), leftX, 200, dt.arcadeWhite);
  renderStringRow(dt.p1Name.substring(0, Math.min(dt.p1Name.length(), 10)), leftX, 240, dt.arcadeOrange);
  renderStringRow("2UP", rightX, 160, dt.arcadeCyan);
  renderStringRow(padZeros(dt.p2Score, 7), rightX, 200, dt.arcadeWhite);
  renderStringRow(dt.p2Name.substring(0, Math.min(dt.p2Name.length(), 10)), rightX, 240, dt.arcadeOrange);
}

// this method will output attempt to estimate what would it look like on the actual display
void preview(FrameData dt) {
  background(0); // led panel are black in colour, so background is black
  renderFrameData(dt);
  // render the preview
  rectMode(CORNER);
  loadPixels();
  for (int x = 0; x < width; x += dt.imgDpSize) {
    for (int y = 0; y < height; y += dt.imgDpSize) {
      int offset = 0; // (int) Math.floor((dt.imgDpSize) / 2);
      color c = pixels[(y + offset) * width + (x + offset)];
      fill(c);
      stroke(0);
      int s = (int) Math.floor(dt.imgDpSize / dt.pixelPitch);
      square(x, y, s);
      noFill();
      noStroke();
    }
  }
}
