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

DeviceRegistry registry;
TestObserver testObserver;

void setup() {
  registry = new DeviceRegistry();
  testObserver = new TestObserver();
  registry.addObserver(testObserver);
}

void draw() {
  if (testObserver.hasStrips) {
    registry.startPushing();
    List<Strip> strips = registry.getStrips();
    // iterate through each available strips
    int i = 0;
    for (Strip strip: strips) {
      println("Strip #" + i++ + ", length: " + strip.getLength());
    }
  } else {
    println("Still waiting for strips!");
  }
}
