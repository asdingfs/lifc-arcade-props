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
FrameDataBuilder builder = new FrameDataBuilder();
FrameData frameData = builder.build();
// load fonts
PFont h1Font;
PFont h2Font;
PFont h3Font;

// START: helper methods for rendering
void resetBackground() {
  background(frameData.arcadeBackground);
}
// END: of helper methods

void setup() {
  size(frameData.widthTotal, frameData.heightTotal);
  resetBackground();
  // initialize registry
  registry = new DeviceRegistry();
  testObserver = new TestObserver();
  registry.addObserver(testObserver);
  // initialize fonts
  h1Font = createFont(frameData.fontName, frameData.h1FontSizePx);
  h2Font = createFont(frameData.fontName, frameData.h2FontSizePx);
  h3Font = createFont(frameData.fontName, frameData.h3FontSizePx);
  // initialize modes
  rectMode(CENTER);
  imageMode(CENTER);
  renderFrameData(frameData);
}

void draw() {
  loadPixels();
  if (testObserver.hasStrips) {
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
  }
}

void renderStringRow(String str, int x, int y, color colour) {
  textAlign(CENTER);
  rectMode(CENTER);
  fill(colour);
  text(str, x, y);
}

void renderFrameData(FrameData dt) {
  // load images
  PImage p1Img = loadImage(dt.p1ImgSrc);
  PImage p2Img = loadImage(dt.p2ImgSrc);
  // resize & fill image to container
  int imgSize = (int) Math.floor(dt.imgContainerSizePx * dt.imgDpSize * dt.imgScale);
  SquareFill p1ImgDim = new SquareFill(p1Img.width, p1Img.height, imgSize);
  SquareCrop p1ImgCrop = new SquareCrop(p1Img.width, p1Img.height, imgSize);
  p1Img.resize(p1ImgDim.w, p1ImgDim.h);
  p1Img = p1Img.get(p1ImgCrop.x, p1ImgCrop.y, p1ImgCrop.w, p1ImgCrop.h);
  SquareFill p2ImgDim = new SquareFill(p2Img.width, p2Img.height, imgSize);
  SquareCrop p2ImgCrop = new SquareCrop(p2Img.width, p2Img.height, imgSize);
  p2Img.resize(p2ImgDim.w, p2ImgDim.h);
  p2Img = p2Img.get(p2ImgCrop.x, p2ImgCrop.y, p2ImgCrop.w, p2ImgCrop.h);
  // render title row
  float row = 1.5;
  textFont(h1Font);
  fill(255);
  renderStringRow(
    "LIFC 2025: RETRO ARCADE",
    dt.widthCenter, 60, dt.arcadeMagenta
  );
}
