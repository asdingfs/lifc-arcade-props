class FrameDataBuilder {
  //VARIABLES
  private String p1Name = "ABCDEFGH";
  private String p1ImgSrc = "imgs/skaev-px.jpg";
  private int p1Score = 1415;
  private String p2Name = "IJKLMOPQ";
  private String p2ImgSrc = "imgs/klyx-px.jpg";
  private int p2Score = 625;
  private int topScore = 0;

  //physical hardware props
  FrameDataBuilder() { }

  FrameDataBuilder p1Name(String name) {
    this.p1Name = formatArcadeStr(name);
    return this;
  }

  FrameDataBuilder p1ImgSrc(String src) {
    this.p1ImgSrc = src;
    return this;
  }

  FrameDataBuilder p1Score(int score) {
    this.p1Score = score;
    return this;
  }

  FrameDataBuilder p2Name(String name) {
    this.p2Name = formatArcadeStr(name);
    return this;
  }

  FrameDataBuilder p2ImgSrc(String src) {
    this.p2ImgSrc = src;
    return this;
  }

  FrameDataBuilder p2Score(int score) {
    this.p2Score = score;
    return this;
  }

  FrameDataBuilder topScore(int score) {
    this.topScore = score;
    return this;
  }

  String formatArcadeStr(String name) {
    int maxLength = 8;
    return name.trim().toUpperCase().substring(0, Math.min(name.length(), maxLength));
  }

  FrameData build() {
    return new FrameData(p1Name, p1ImgSrc, p1Score, p2Name, p2ImgSrc, p2Score, topScore);
  }
}
