class FrameData {
  // VARIABLES
  private String p1Name;
  private String p1ImgSrc;
  private int p1Score;
  private String p2Name;
  private String p2ImgSrc;
  private int p2Score;
  private int topScore;
  // CONSTANTS
  // hardware
  private int ledPanelHeight = 64;
  private int ledPanelWidth = 64;
  private int ledPanelCount = 5;
  // images
  private int imgContainerSize = 64;
  private int imgDpSize = 4;
  private float imgScale = 0.9;
  // fonts
  private String fontName = "nintendo-nes-font.ttf";
  private int rowSizePx = 40;
  private int h1FontSizePx = 32;
  private int h2FontSizePx = 32;
  private int h3FontSize = 16;
  // colours
  private color arcadeBackground = color(11, 11, 53);
  private color arcadeWhite = color(255, 228, 250);
  private color arcadeRed = color(229, 35, 53);
  private color arcadeCyan = color(93, 235, 255);
  private color arcadeOrange = color(255, 152, 4);
  private color arcadeMagenta = color(255, 97, 199);
  // pixellation parameters (this is only for display)
  private float pixelPitch = 1.05;
  private int pixellationSize = 1;

  // CONSTRUCTORS
  FrameData(
    String p1Name,
    String p1ImgSrc,
    int p1Score,
    String p2Name,
    String p2ImgSrc,
    int p2Score,
    int topScore
  ) {
    this.p1Name = p1Name;
    this.p1ImgSrc = p1ImgSrc;
    this.p1Score = p1Score;
    this.p2Name = p2Name;
    this.p2ImgSrc = p2ImgSrc;
    this.p2Score = p2Score;
    this.topScore = topScore;
  }
}
