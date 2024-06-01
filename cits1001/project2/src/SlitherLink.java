
/**
 * SlitherLink does the user interaction for a square Slither Link puzzle.
 * 
 * @author Thomas Cleary
 * @version v2.00
 */
import java.awt.*;
import java.awt.event.*;

public class SlitherLink implements MouseListener
{    
    private Puzzle game;     // internal representation of the game
    private SimpleCanvas sc; // the display window
    
    private final int scWidth     = 800;
    private final int scHeight    = 1000; 
    private final int puzzleWidth = 660;
    private final int offSet      = 70;
    private final int buttonTop   = scWidth + 75;
    private final int buttonJoin  = scWidth / 2;
    private final int buttonGap   = 3;

    private final Font buttonFont = new Font("Times", 20, 70);
    private final Font bannerFont = new Font("Times", 20, 49);

    private final Color bgColor      = new Color(250, 245, 235);
    private final Color dotColor     = new Color(142, 115, 86);
    private final Color textColor    = new Color(142, 115, 86);
    private final Color textColor2   = new Color(250, 245, 235);
    private final Color onColor      = new Color(131, 159, 86);
    private final Color offColor     = new Color(162, 179, 104, 25);
    private final Color bannerColor  = new Color(142, 115, 86);
    private final Color buttonColor  = new Color(162, 179, 104);
    private final Color buttonColor2 = new Color(255, 164, 92);
    
    private int squareSize;
    private int dotRadius;
    
    private String feedback;
    
    private Font numFont;
    
    /**
     * Creates a display for playing the puzzle p.
     */
    public SlitherLink(Puzzle p)
    {
        game = p;
        
        squareSize = puzzleWidth / p.size();

        // Must be < 0.2 * squareSize otherwise dotRadius bigger than offSet
        // for 2x2 puzzle.
        dotRadius  = (int) (squareSize * 0.15);

        numFont = new Font("Times", 20, 3 * dotRadius);
        
        sc = new SimpleCanvas("Slither Link", scWidth, scHeight, bgColor);
        sc.addMouseListener(this);
        
        feedback = "Good Luck";
        
        drawNums();
        drawBanner();
        drawButtons();
        
        displayPuzzle();
    }
    
    /**
     * Returns the current state of the game.
     */
    public Puzzle getGame()
    {
        return game;
    }

    /**
     * Returns the current state of the canvas.
     */
    public SimpleCanvas getCanvas()
    {
        return sc;
    }

    /**
     * Displays the initial puzzle on sc. 
     * Have a look at puzzle-loop.com for a basic display,
     * or use your imagination.
     */
    public void displayPuzzle()
    {
        drawLines();
        drawDots();
    }
    
    private void drawLines()
    {
        int rowCoord1;
        int rowCoord2;
        int colCoord1;
        int colCoord2;
        
        Color lineColor;
        
        // Draw horizontal lines
        for(int row = 0; row <= game.size(); row++) {
            rowCoord1 = (row * squareSize) + offSet - (dotRadius / 2);
            rowCoord2 = (row * squareSize) + offSet + (dotRadius / 2);
            
            for(int col = 0; col < game.size(); col++) {
                colCoord1 = (col * squareSize)       + offSet + (dotRadius / 2);
                colCoord2 = ((col + 1) * squareSize) + offSet - (dotRadius / 2);
                
                if(game.getHorizontal()[row][col]) {
                    lineColor = onColor;
                }
                else {
                    lineColor = offColor;
                    
                    // Draw "off" line.
                    sc.drawRectangle(colCoord1, rowCoord1,
                                     colCoord2, rowCoord2, bgColor);
                }
                
                sc.drawRectangle(colCoord1, rowCoord1,
                                 colCoord2, rowCoord2, lineColor);
            }
        }
        
        // Draw vertical lines
        for(int row = 0; row < game.size(); row++) {
            rowCoord1 = (row * squareSize)       + offSet + (dotRadius / 2);
            rowCoord2 = ((row + 1) * squareSize) + offSet - (dotRadius / 2);
            
            for(int col = 0; col <= game.size(); col++) {
                colCoord1 = (col * squareSize) + offSet - (dotRadius / 2);
                colCoord2 = (col * squareSize) + offSet + (dotRadius / 2);
                
                if(game.getVertical()[row][col]) {
                    lineColor = onColor;
                }
                else {
                    lineColor = offColor;
                    
                    // Draw "off" line.
                    sc.drawRectangle(colCoord1, rowCoord1,
                                     colCoord2, rowCoord2, bgColor);
                }
                
                sc.drawRectangle(colCoord1, rowCoord1,
                                 colCoord2, rowCoord2, lineColor);
            }
        }
    }
    
    private void drawDots()
    {
        for(int row = 0; row < game.size() + 1; row++) {
            int rowCoord = (row * squareSize) + offSet;
            
            for(int col = 0; col < game.size() + 1; col++) {
                int colCoord = (col * squareSize) + offSet;

                sc.drawDisc(colCoord, rowCoord, dotRadius, dotColor);
            }
        }
    }
    
    private void drawNums()
    {
        sc.setFont(numFont);
        
        int adjustment = (int) (squareSize * 0.13);
        
        for(int row = 0; row < game.size(); row++) {
            int rowCoord = (row * squareSize) + (squareSize / 2)
                         + offSet + adjustment;
            
            for(int col = 0; col < game.size(); col++) {
                int colCoord = (col * squareSize) + (squareSize / 2)
                             + offSet - adjustment;

                int square = game.getPuzzle()[row][col];
                
                if(square >= 0 && square < 4) {
                    sc.drawString(square, colCoord, rowCoord, textColor);
                }
            }
        }
    }
    
    private void drawBanner()
    {
        sc.setFont(bannerFont);
        
        sc.drawRectangle(0, scWidth, scWidth, buttonTop, bannerColor);
        
        int adjustment = 10;
        sc.drawString(feedback, adjustment,
                      buttonTop - (2 * adjustment), textColor2);
    }
    
    private void drawButtons()
    {
        sc.setFont(buttonFont);
        
        int xAdj = 120;
        int yAdj = 25;
        
        // Clear button
        sc.drawRectangle(0, buttonTop,
                         buttonJoin, scHeight,
                         buttonColor2);

        sc.drawString("CLEAR",
                      (scWidth / 4) - xAdj,
                      ((scHeight + buttonTop) / 2) + yAdj,
                      textColor);
        
        // Check button
        sc.drawRectangle(buttonJoin, buttonTop,
                         scWidth, scHeight,
                         buttonColor);

        sc.drawString("CHECK",
                      (int)((scWidth * 0.75) - xAdj),
                      ((scHeight + buttonTop) / 2) + yAdj,
                      textColor);
    }
    
    /**
     * Makes a horizontal click to the right of Dot r,c.
     * Update game and the display, if the indices are legal;
     * otherwise do nothing.
     */
    public void horizontalClick(int r, int c)
    {
        if(r >= 0 && r < game.size() + 1) {
            if(c >= 0 && c < game.size()) {
                game.horizontalClick(r, c);
                displayPuzzle();
            }
        }
    }
    
    /**
     * Makes a vertical click below Dot r,c. 
     * Update game and the display, if the indices are legal;
     * otherwise do nothing.
     */
    public void verticalClick(int r, int c)
    {
        if(r >= 0 && r < game.size()) {
            if(c >= 0 && c < game.size() + 1) {
                game.verticalClick(r, c);
                displayPuzzle();
            }
        }
    }
    
    /**
     * Checks to see if a mouse click corresponds to a puzzle line.
     */
    private void checkLines(MouseEvent e)
    {
        int colLowerBound = offSet - dotRadius;
        int colUpperBound = colLowerBound + squareSize;
        
        int rowLowerBound;
        int rowUpperBound;
        
        int diameter   = 2 * dotRadius;
        
        int xMouse = e.getX();
        int yMouse = e.getY();
        
        outerLoop:
        for(int col = 0; col <= game.size(); col++) {

            // is click within this column?
            if(xMouse > colLowerBound && xMouse < colUpperBound) {

                // is click within vertical line part of column?
                if(xMouse < colLowerBound + diameter) {
                    rowLowerBound = offSet + dotRadius;
                    rowUpperBound = rowLowerBound + squareSize - diameter;

                    // is click within vertical line space of this row?
                    for(int row = 0; row < game.size(); row++) {
                        if(yMouse > rowLowerBound && yMouse < rowUpperBound) {
                            verticalClick(row, col);
                            displayPuzzle();
                            break outerLoop; // found line, stop looking
                        }
                        // check next row
                        else {
                            rowLowerBound += squareSize;
                            rowUpperBound += squareSize;
                        }
                    }
                }
                // is click in valid horizontal lines space of this column?
                else if(col < game.size()) {
                    rowLowerBound = offSet - dotRadius;
                    rowUpperBound = rowLowerBound + diameter;

                    // is click within horizontal line space of this row?
                    for(int row = 0; row <= game.size(); row++) {
                        if(yMouse > rowLowerBound && yMouse < rowUpperBound) {
                            horizontalClick(row, col);
                            displayPuzzle();
                            break outerLoop; // found line, stop looking
                        }
                        // check next row
                        else {
                            rowLowerBound += squareSize;
                            rowUpperBound += squareSize;
                        }
                    }
                }
            }
            // check next column
            else {
                colLowerBound += squareSize;
                colUpperBound += squareSize;
            }
        }
    }
    
    /**
     * Checks if a mouse click corresponds to a button
     */
    private void checkButtons(MouseEvent e)
    {
        int xMouse = e.getX();
        int yMouse = e.getY();
        
        if(yMouse > buttonTop && yMouse < scHeight) {
            if(xMouse > 0 && xMouse < (buttonJoin - buttonGap)) {
                game.clear();
                displayPuzzle();
            }
            feedback = AnalyzeSolution.finished(game);
            drawBanner();
        }
    }
    
    /**
     * Actions for a mouse press.
     */
    public void mousePressed(MouseEvent e) 
    {
        checkLines(e);
        checkButtons(e);
    }
    public void mouseClicked(MouseEvent e) {}
    public void mouseReleased(MouseEvent e) {}
    public void mouseEntered(MouseEvent e) {}
    public void mouseExited(MouseEvent e) {}
}
