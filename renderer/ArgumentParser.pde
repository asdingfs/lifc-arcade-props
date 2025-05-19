class ArgumentParser {
  HashMap<String, String> options = new HashMap<>();

  ArgumentParser(String[] args) {
    for (String arg : args) {
      if (arg.startsWith("--")) {
        String[] split = arg.substring(2).split("=");
        if (split.length == 2) {
          this.options.put(split[0], split[1]);
        }
      }
      // else, skip if it's not a valid argument
    }
  }

  boolean toSavePreview() {
    String savePreview = options.get("savePreview");
    return savePreview != null && !savePreview.trim().isEmpty();
  }

  String getSavePreviewLocation() { 
    return options.get("savePreview");
  }

  FrameData toFrameData() {
    String p1Name = options.get("p1Name");
    String p1ImgSrc = options.get("p1ImgSrc");
    String p1ScoreStr = options.get("p1Score");
    String p2Name = options.get("p2Name");
    String p2ImgSrc = options.get("p2ImgSrc");
    String p2ScoreStr = options.get("p2Score");
    String topScoreStr = options.get("topScore");

    FrameDataBuilder builder = new FrameDataBuilder();
    if (p1Name != null && !p1Name.trim().isEmpty()) { builder.p1Name(p1Name); }
    if (p1ImgSrc != null && !p1ImgSrc.trim().isEmpty()) { builder.p1ImgSrc(p1ImgSrc); }
    if (p1ScoreStr != null && !p1ScoreStr.trim().isEmpty()) {
      try {
        int p1Score = Integer.parseInt(p1ScoreStr);
        builder.p1Score(p1Score);
      } catch (NumberFormatException e) {
        println("Invalid p1Score: " + p1ScoreStr);
      }
    }
    if (p2Name != null && !p2Name.trim().isEmpty()) { builder.p2Name(p2Name); }
    if (p2ImgSrc != null && !p2ImgSrc.trim().isEmpty()) { builder.p2ImgSrc(p2ImgSrc); }
    if (p2ScoreStr != null && !p2ScoreStr.trim().isEmpty()) {
      try {
        int p2Score = Integer.parseInt(p2ScoreStr);
        builder.p2Score(p2Score);
      } catch (NumberFormatException e) {
        println("Invalid p2Score: " + p2ScoreStr);
      }
    }
    if (topScoreStr != null && !topScoreStr.trim().isEmpty()) {
      try {
        int topScore = Integer.parseInt(topScoreStr);
        builder.topScore(topScore);
      } catch (NumberFormatException e) {
        println("Invalid topScore: " + topScoreStr);
      }
    }
    return builder.build();
  }
}
