class SquareFill {
  private int w;
  private int h;

  SquareFill(int w, int h) {
    this.w = w;
    this.h = h;
  }

  SquareFill(int oW, int oH, int toSize) {
    float scale = (float) toSize / Math.min(oW, oH);
    this.w = (int) Math.floor(oW * scale);
    this.h = (int) Math.floor(oH * scale);
  }
}
