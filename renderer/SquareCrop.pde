class SquareCrop {
  private int x;
  private int y;
  private int w;
  private int h;

  SquareCrop(int oW, int oH, int boxSize) {
    int boxCenter = (int) Math.floorDiv(boxSize, 2);
    this.x = Math.max(Math.floorDiv(oW, 2) - boxCenter, 0);
    this.y = Math.max(Math.floorDiv(oH, 2) - boxCenter, 0);
    this.w = Math.min(boxSize, oW);
    this.h = Math.min(boxSize, oH);
  }
}
