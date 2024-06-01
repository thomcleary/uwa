// Thomas Cleary (21704985)

import java.util.PriorityQueue;
import java.util.Comparator;

public class MyProject implements Project {


    public MyProject() {}


    /**
     * Determines the number of pixels that would be converted to black in a
     * black flood fill beginning at pixel (row, col)
     * @param image the int[][] representing a greyscale image
     * @param row the row of the source pixel
     * @param col the column of the source pixel
     * @return an integer value of how many pixels where changed to black
     */
    public int floodFillCount(int[][] image, int row, int col) {
        int sourceColour = image[row][col];
        int filled = 0;

        if (sourceColour == 0) return 0; // source already Black
             
        filled = floodFillCount(image, row, col, filled, sourceColour);  
        return filled;
    }


    /**
     * Method to recursivley perform a depth first search to black flood fill
     * all pixels of sourceColour starting at pixel (row, col)
     * @param image the greyscale image
     * @param row the row of the source pixel in image
     * @param col the column of the source pixel in image
     * @param filled how many pixels have been filled so far
     * @param sourceColour the colour of the original starting pixel
     * @return the number of pixels converted to black
     */
    private int floodFillCount(int[][] image, int row, int col, 
                               int filled, int sourceColour) {
        image[row][col] = 0; // set source pixel to black
        filled++;

        int[][] adjacentPixels = new int[][] {
            {row+1, col}, // down
            {row-1, col}, // up
            {row, col+1}, // right
            {row, col-1}  // left
        };

        for (int[] adjPixel : adjacentPixels) {
            int adjPixelRow = adjPixel[0];
            int adjPixelCol = adjPixel[1];
            
            // if legal pixel
            if (adjPixelRow >= 0 && adjPixelRow < image.length &&
                adjPixelCol >= 0 && adjPixelCol < image[0].length) {
                // if pixel same colour as source
                if (image[adjPixelRow][adjPixelCol] == sourceColour) {
                    filled = floodFillCount(image,
                                            adjPixelRow, adjPixelCol,
                                            filled, sourceColour);
                }
            }
        }
        return filled;
    }


    /**
     * Determine the brightness of the brightest k*k square in image
     * @param image the greyscale image
     * @param k the side length of the square size to check for
     * @return the brightness of the brightes k*k square
     */
    public int brightestSquare(int[][] image, int k) {
        int imageHeight = image.length;
        int imageWidth  = image[0].length;
        int brightest   = 0;
        int startRow    = 0;
        int endRow      = startRow + k - 1;

        // while square not shifted past bottom of image
        while (endRow < imageHeight) {
            int[] columnSums = new int[imageWidth];

            // calculate sums of columns in image between start and end row
            // and store in columnSums
            for (int col = 0; col < imageWidth; col++) {
                int columnSum = 0;
                for (int row = startRow; row <= endRow; row++) {
                    columnSum += image[row][col];
                }
                columnSums[col] = columnSum;
            }
            int lastValidIndex = columnSums.length - k;

            // calculate the brightness of each square between start and end
            // row
            for (int i = 0; i <= lastValidIndex; i++) {
                int squareSum = 0;
                for (int j = i; j < i + k; j++) {
                    squareSum += columnSums[j];
                }
                if (squareSum > brightest) brightest = squareSum;
            }
            // shift square down one pixel
            startRow++;
            endRow++;
        }
        return brightest;
    }


    public int darkestPath(int[][] image, int ur, int uc, int vr, int vc) {
        PriorityQueue<int[][]> pixelQueue = new PriorityQueue<>(
                                                    1,
                                                    new PixelComparator()
                                                );

        pixelQueue.add(new int[][] {{image[ur][uc]}, {ur, uc}});

        boolean[][] searched = new boolean[image.length][image[0].length];
        searched[ur][uc] = true;

        // set inital brightest pixel to brighter of start or end pixel
        int brightness;
        if (image[ur][uc] >= image[vr][vc]) {
            brightness = image[ur][uc];
        }
        else {
            brightness = image[vr][vc];
        }

        boolean endPixelFound = false;

        // while pixel (vr, vc) has not been encountered as an adjacent pixel
        while (!endPixelFound) {
            // get next darkest unvisited pixel on we have encountered as
            // an adjacent pixel
            int[][] currPixel = pixelQueue.poll();
            int currPixelBness = currPixel[0][0];
            int currPixelRow = currPixel[1][0];
            int currPixelCol = currPixel[1][1];
            
            if (currPixelBness > brightness) brightness = currPixelBness;

            int[][] adjacentPixels = new int[][] {
                {currPixelRow+1, currPixelCol}, // down
                {currPixelRow-1, currPixelCol}, // up
                {currPixelRow,   currPixelCol+1}, // right
                {currPixelRow,   currPixelCol-1}  // left
            };

            for (int[] adjPixel : adjacentPixels) {
                int adjPixelRow = adjPixel[0];
                int adjPixelCol = adjPixel[1];

                if (adjPixelRow == vr && adjPixelCol == vc) {
                    endPixelFound = true; // end pixel is adjacent to current
                }
                
                if (!endPixelFound) {
                    // if legal pixel
                    if (adjPixelRow >= 0 && adjPixelRow < image.length &&
                        adjPixelCol >= 0 && adjPixelCol < image[0].length) {

                            // if pixel not added to queue before
                            if (!searched[adjPixelRow][adjPixelCol]) {
                                pixelQueue.add(new int[][] {
                                    {image[adjPixelRow][adjPixelCol]},
                                    {adjPixelRow, adjPixelCol}
                                });
                                searched[adjPixelRow][adjPixelCol] = true;
                            }
                        }
                    }
                }
            }
        return brightness;
    }


    /**
     * Class to compare int[][] that represent a pixels' coordinates in image
     * and their brightness
     * eg. pixel at [2,3] with brightness 7 -> [[7], [2,3]]
     */
    public class PixelComparator implements Comparator<int[][]> {

        public int compare(int[][] pixel1, int[][] pixel2) {
            if      (pixel1[0][0] < pixel2[0][0]) return -1;
            else if (pixel1[0][0] > pixel2[0][0]) return  1;
            return  0;
        }
    }


    /**
     * For each query in queries, finds the brightest in the defined row
     * segment of image.
     * @param image the greyscale image
     * @param queries the list of queries to compute brightnesses for
     * @return the brightest pixel in a row segment defined in each query in
     * queries
     */
    public int[] brightestPixelsInRowSegments(int[][] image, int[][] queries) {
        int[] brightestPixels = new int[queries.length];
        int queryNum = 0;

        for (int[] query : queries) {
            int row      = query[0];
            int startCol = query[1];
            int endCol   = query[2];

            int brightest = 0;

            // for each pixel in the row segment defined in query
            for (int pixel = startCol; pixel < endCol; pixel++) {
                int pixelBness = image[row][pixel];
                if (pixelBness > brightest) brightest = pixelBness;
            }
            brightestPixels[queryNum++] = brightest;
        }
        return brightestPixels;
    }
}