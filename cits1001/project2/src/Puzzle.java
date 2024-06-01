
/**
 * Puzzle maintains the internal representation of a square Slither Link puzzle.
 * 
 * @author Thomas Cleary
 * @version v2.00
 */
import java.util.ArrayList;

public class Puzzle
{
    private int[][] puzzle;         // the numbers in the squares, i.e. the
                                    // puzzle definition
                                    // -1 if the square is empty, 0-3 otherwise
    private boolean[][] horizontal; // the horizontal line segments in the
                                    // current solution
                                    // true if the segment is on,
                                    // false otherwise
    private boolean[][] vertical;   // the vertical line segments in the
                                    // current solution
                                    // true if the segment is on,
                                    // false otherwise

    /**
     * Creates the puzzle from file filename, and an empty solution.
     * filename is assumed to hold a valid puzzle.
     */
    public Puzzle(String filename)
    {
        FileIO gameFile = new FileIO(filename);
        
        parseFile(gameFile.getLines());
        
        horizontal = new boolean[size() + 1][size()];
        vertical   = new boolean[size()][size() + 1];
    }
    
    /**
     * Creates the puzzle from "eg3_1.txt".
     */
    public Puzzle()
    {
        this("eg5_2.txt");
    }

    /**
     * Returns the size of the puzzle.
     */
    public int size()
    {
        return puzzle.length;
    }

    /**
     * Returns the number layout of the puzzle.
     */
    public int[][] getPuzzle()
    {
        return puzzle;
    }

    /**
     * Returns the state of the current solution, horizontally.
     */
    public boolean[][] getHorizontal()
    {
        return horizontal;
    }

    /**
     * Returns the state of the current solution, vertically.
     */
    public boolean[][] getVertical()
    {
        return vertical;
    }

    /**
     * Turns lines into a Slither Link puzzle.
     * Each String holds one line from the input file. 
     * The first String in the argument goes into puzzle[0], 
     * The second String goes into puzzle[1], etc. 
     * lines is assumed to hold a valid square puzzle;
     * see eg3_1.txt and eg5_1.txt for examples.
     */
    public void parseFile(ArrayList<String> lines)
    {
        puzzle = new int[lines.size()][lines.size()];
        
        int row = 0;
        for(String line : lines) {
            String[] squares = line.split(" ");
            int col = 0;
            for(String squareValue : squares) {
                Integer squareNum = Integer.valueOf(squareValue);
                puzzle[row][col] = squareNum.intValue();
                col++;
            }
            row++;
        }
    }
    
    /**
     * Toggles the horizontal line segment to the right of Dot r,c,
     * if the indices are legal.
     * Otherwise do nothing.
     */
    public void horizontalClick(int r, int c)
    {
        if(r <= size() && c < size()) {
            horizontal[r][c] = !horizontal[r][c];
        }
    }
    
    /**
     * Toggles the vertical line segment below Dot r,c,
     * if the indices are legal.
     * Otherwise do nothing.
     */
    public void verticalClick(int r, int c)
    {
        if(r < size() && c <= size()) {
            vertical[r][c] = !vertical[r][c];
        }
    }
    
    /**
     * Clears all line segments out of the current solution.
     */
    public void clear()
    {
        for(int row = 0; row < size() + 1; row++) {
            for(int col = 0; col < size(); col++) {
                if(horizontal[row][col]) {
                    horizontal[row][col] = !horizontal[row][col];
                }
            }
        }
    
        for(int row = 0; row < size(); row++) {
            for(int col = 0; col < size() + 1; col++) {
                if(vertical[row][col]) {
                    vertical[row][col] = !vertical[row][col];
                }
            }
        }
    }
}
