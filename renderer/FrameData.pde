class FrameData {
  //VARIABLES
  private String p1Name;
  private String p1ImgSrc;
  private int p1Score;
  private String p2Name;
  private String p2ImgSrc;
  private int p2Score;
  private int topScore;
  //CONSTANTS
  //hardware
  static final private int ledPanelHeight = 64;
  static final private int ledPanelWidth = 64;
  static final private int ledPanelHCount = 5; // tiled horizontally
  static final private int ledPanelVCount = 1; // tiled vertically
  //images
  static final private int imgContainerSizePx = 64;
  static final private int imgDpSize = 4;
  static final private float imgScale = 0.9;
  //positions
  static final private int widthTotal = ledPanelWidth * ledPanelHCount * imgDpSize;
  final private int widthCenter = Math.floorDiv(ledPanelWidth * ledPanelHCount, 2) * imgDpSize;
  static final private int heightTotal = ledPanelHeight * ledPanelVCount * imgDpSize;
  final private int heightCenter = Math.floorDiv(ledPanelHeight * ledPanelVCount, 2) * imgDpSize;
  //fonts
  static final private String fontName = "nintendo-nes-font.ttf";
  static final private int h1FontSizePx = 32;
  static final private int h2FontSizePx = 32;
  static final private int h3FontSizePx = 16;
  //colours
  final private color arcadeBackground = color(11, 11, 53);
  final private color arcadeWhite = color(255, 228, 250);
  final private color arcadeRed = color(229, 35, 53);
  final private color arcadeCyan = color(93, 235, 255);
  final private color arcadeOrange = color(255, 152, 4);
  final private color arcadeMagenta = color(255, 97, 199);
  //pixellation parameters (this is only for display)
  final private float pixelPitch = 1.05;
  final private int pixellationSize = 1;

  //CONSTRUCTORS
  FrameData(String p1Name, String p1ImgSrc, int p1Score, String p2Name, String p2ImgSrc, int p2Score, int topScore) {
    this.p1Name = p1Name;
    this.p1ImgSrc = p1ImgSrc;
    this.p1Score = p1Score;
    this.p2Name = p2Name;
    this.p2ImgSrc = p2ImgSrc;
    this.p2Score = p2Score;
    this.topScore = topScore;
  }
}
