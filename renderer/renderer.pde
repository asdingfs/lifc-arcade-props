import com.heroicrobot.controlsynthesis.*;
import com.heroicrobot.dropbit.discovery.*;
import com.heroicrobot.dropbit.common.*;
import com.heroicrobot.dropbit.registry.*;
import com.heroicrobot.dropbit.devices.*;
import com.heroicrobot.dropbit.devices.pixelpusher.*;
import FrameData;
import Animation;
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

DeviceRegistry registry;
TestObserver testObserver;
FrameData.Builder frameDataBuilder;
FrameData frameData;

// TEST START: ANIMATION
Animation animation1, animation2;
float xpos;
float ypos;
// TEST END: ANIMATION


void setup() {
  // registry
  registry = new DeviceRegistry();
  testObserver = new TestObserver();
  registry.addObserver(testObserver);
  frameDataBuilder = new FrameData.Builder();
  frameData = frameDataBuilder.build();
  // TEST START: ANIMATION
  size(320, 320);
  background(255, 204, 0);
  frameRate(24);
  animation1 = new Animation("PT_Shifty_", 38);
  animation2 = new Animation("PT_Teddy_", 60);
  xpos = width * 0.75;
  ypos = height * 0.5;
  // TEST END: ANIMATION
}

void draw() {
  // TEST START: ANIMATION
  // Display the sprite at the position xpos, ypos
  if (mousePressed) {
    background(153, 153, 0);
    animation1.display(xpos-animation1.getWidth()/2, ypos);
  } else {
    background(255, 204, 0);
    animation2.display(xpos-animation1.getWidth()/2, ypos);
  }
  loadPixels();
  // TEST END: ANIMATION
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
