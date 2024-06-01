
/**
 * AnalyzeSolution methods are used to analyze the state of a Slither Link puzzle, 
 * to determine if the puzzle is finished. 
 * 
 * @author Thomas Cleary
 * @version v2.00
 */
import java.util.*;

public class AnalyzeSolution
{
    /**
     * We don't need to create any objects of class AnalyzeSolution; all of its
     * methods are static.
     */
    private AnalyzeSolution() {}

    /**
     * Returns the number of line segments surrounding Square r,c in p.
     * Returns 0 if the indices are illegal.
     */
    public static int linesAroundSquare(Puzzle p, int r, int c)
    {
        int puzzleSize = p.size();
        
        if(r > puzzleSize && r < 0 && c > puzzleSize && c < 0) { // Should be or
            return 0;
        }
        else {
            int numLines = 0;
            
            boolean[][] puzzleHor = p.getHorizontal();
            boolean[][] puzzleVer = p.getVertical();
            
            if(puzzleHor[r][c])   numLines++;
            if(puzzleHor[r+1][c]) numLines++;
            if(puzzleVer[r][c])   numLines++;
            if(puzzleVer[r][c+1]) numLines++;
            
            return numLines;
        }
    }
    
    /**
     * Returns all squares in p that are surrounded by the wrong number of line
     * segments.
     * Each item on the result will be an int[2] containing the indices of a
     * square.
     * The order of the items on the result is unimportant.
     */
    public static ArrayList<int[]> badSquares(Puzzle p)
    {
        ArrayList<int[]> badSquares = new ArrayList<>();
        
        int puzzleSize = p.size();
        
        for(int row = 0; row < puzzleSize; row++) {
            for(int col = 0; col < puzzleSize; col++) {
                int squareValue = p.getPuzzle()[row][col];
                
                if(squareValue != -1) {
                    if(squareValue != linesAroundSquare(p, row, col)) {
                        badSquares.add(new int[]{row, col});
                    }
                }
            }
        }
        
        return badSquares;
    }

    /**
     * Returns all dots connected by a single line segment to Dot r,c in p.
     * Each item on the result will be an int[2] containing the indices of a
     * dot.
     * The order of the items on the result is unimportant.
     * Returns null if the indices are illegal.
     */
    public static ArrayList<int[]> getConnections(Puzzle p, int r, int c)
    {
        int puzzleSize = p.size();
        
        if(r < 0 && r > puzzleSize && c < 0 && c > puzzleSize) { // These should be or
            return null;
        }
        
        ArrayList<int[]> connectedDots = new ArrayList<>();
        
        boolean[][] horizontalLines = p.getHorizontal();
        boolean[][] verticalLines   = p.getVertical();
        
        if(c > 0) {
            if(horizontalLines[r][c-1]) connectedDots.add(new int[]{r, c-1});
        }
        
        if(c < puzzleSize) {
            if(horizontalLines[r][c])   connectedDots.add(new int[]{r, c+1});
        }
        
        if(r > 0) {
            if(verticalLines[r-1][c])   connectedDots.add(new int[]{r-1, c});
        }
        
        if(r < puzzleSize) {
            if(verticalLines[r][c])     connectedDots.add(new int[]{r+1, c});
        }
        
        return connectedDots; 
    }

    /**
     * Returns an array of length 3 whose first element is the number of line
     * segments in the puzzle p, and whose other elements are the indices of a
     * dot on any one of those segments.
     * Returns {0,0,0} if there are no line segments on the board. 
     */
    public static int[] lineSegments(Puzzle p)
    {
        int onDotRow = 0;
        int onDotCol = 0;
        int lines    = 0;
        
        boolean[][] horizontalLines = p.getHorizontal();
        boolean[][] verticalLines   = p.getVertical();
        
        int puzzleSize = p.size();
        
        for(int row = 0; row <= puzzleSize; row++) {
            for(int col = 0; col <= puzzleSize; col++) {
                if(col < puzzleSize) {
                    if(horizontalLines[row][col]) {
                        onDotRow = row;
                        onDotCol = col;
                        lines++;
                    }
                }
                if(row < puzzleSize) {
                    if(verticalLines[row][col]) {
                        onDotRow = row;
                        onDotCol = col;
                        lines++;
                    }
                }
            }
        }
        
        return new int[]{lines, onDotRow, onDotCol};
    }
    
    /**
     * Tries to trace a closed loop starting from Dot r,c in p. 
     * Returns either an appropriate error message, or 
     * the number of steps in the closed loop (as a String). 
     * See the project page and the JUnit for a description of the messages
     * expected.
     */
    public static String tracePath(Puzzle p, int r, int c)
    {
        ArrayList<int[]> connections = getConnections(p, r, c);
        
        int rowStart = r;
        int colStart = c;
        
        int rowPrev = r;
        int colPrev = c;
        
        int rowCurr = r;
        int colCurr = c;
        
        int steps = 0;
        
        if(connections.size() == 0) return "No path";
        
        do {
            connections = getConnections(p, rowCurr, colCurr);
            if(connections.size() > 2)  return "Branching line";
            
            boolean newDotFound = false;
            
            for(int[] connection : connections) {
                int rowConnection = connection[0];
                int colConnection = connection[1];
                
                if(rowConnection != rowPrev || colConnection != colPrev) {
                    newDotFound = !newDotFound;
                    
                    rowPrev = rowCurr;
                    colPrev = colCurr;
                    
                    rowCurr = rowConnection;
                    colCurr = colConnection;
                    
                    steps++;
                    break;
                }
            }
            
            if(!newDotFound) return "Dangling end";
        } 
        while(rowCurr != rowStart || colCurr != colStart);  
        
        return String.valueOf(steps); 
    }
    
    /**
     * Returns a message on whether the puzzle p is finished. 
     * p is finished iff all squares are good, and all line segments form a
     * single closed loop.
     * An algorithm is given on the project page. 
     * See the project page and the JUnit for a description of the messages
     * expected.
     */
    public static String finished(Puzzle p)
    {
        if(badSquares(p).size() > 0) {
            return "Wrong number";
        }
        
        int[] line = lineSegments(p);
        
        int numLines = line[0];
        
        int lineRow = line[1];
        int lineCol = line[2];
        
        String trace = tracePath(p, lineRow, lineCol);
        
        if(trace.equals("Branching line") || trace.equals("Dangling end")) {
            return trace;
        }
        
        int traceNum = Integer.parseInt(trace);
        
        if(numLines > traceNum) {
            return "Disconnected lines";
        }
        
        return "Finished";
    }
}
