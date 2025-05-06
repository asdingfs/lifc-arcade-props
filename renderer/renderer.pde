import com.heroicrobot.controlsynthesis.*;
import com.heroicrobot.dropbit.discovery.*;
import com.heroicrobot.dropbit.common.*;
import com.heroicrobot.dropbit.registry.*;
import com.heroicrobot.dropbit.devices.*;
import com.heroicrobot.dropbit.devices.pixelpusher.*;
import FrameData;
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
FrameData frameData;

void setup() {
  // registry
  registry = new DeviceRegistry();
  testObserver = new TestObserver();
  registry.addObserver(testObserver);
  frameData = (new FrameData.Builder()).build();
}

void draw() {
  if (testObserver.hasStrips) {
    registry.startPushing();
    List<Strip> strips = registry.getStrips();
    // iterate through each available strips
    for (Strip strip: strips) {
      // draw on each strip here
    }
  }
}
