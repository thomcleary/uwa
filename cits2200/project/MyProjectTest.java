public class MyProjectTest {

    int passed = 0;

    public void printResult(int got, int expected) {
        System.out.println("Got: " + got);
        System.out.println("Expected: " + expected);
        if (got == expected){
            System.out.println("PASS");
            passed++;
        }
        else {
            System.out.println("FAIL");
        }
        System.out.println();
    }
    
    public static void main(String[] args) {
        MyProject     prj  = new MyProject();
        MyProjectTest test = new MyProjectTest();

        int[][] image = new int[][] {
            {1, 1, 1, 3},
            {0, 1, 2, 3},
            {0, 1, 2, 3},
            {3, 1, 3, 3}
        };
        int testNum = 1;

        System.out.println("floodFillCount() Test " + testNum++);
        int got = prj.floodFillCount(image, 0, 0);
        int expected = 6;
        test.printResult(got, expected);

        System.out.println("floodFillCount() Test " + testNum++);
        got = prj.floodFillCount(image, 1, 0);
        expected = 0;
        test.printResult(got, expected);

        System.out.println("floodFillCount() Test " + testNum++);
        got = prj.floodFillCount(image, 2, 2);
        expected = 2;
        test.printResult(got, expected);

        System.out.println("floodFillCount() Test " + testNum++);
        got = prj.floodFillCount(image, 3, 3);
        expected = 5;
        test.printResult(got, expected);

        // brightestSquare()
        image = new int[][] {
            {1, 1, 1, 3},
            {0, 1, 2, 3},
            {0, 1, 2, 3},
            {3, 1, 3, 3}
        };

        int[][] largeImage = new int[][] {
            {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 2, 1, 1, 1, 1, 1, 0, 0},
            {0, 0, 1, 1, 1, 1, 1, 1, 0, 0},
            {0, 0, 1, 1, 1, 1, 1, 1, 0, 0},
            {0, 0, 1, 1, 1, 1, 1, 1, 0, 0},
            {0, 0, 1, 1, 1, 1, 1, 1, 0, 0},
            {0, 0, 1, 1, 1, 1, 1, 1, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 1, 1, 1, 1, 1, 1, 0, 0},
            {0, 0, 1, 1, 1, 1, 1, 1, 0, 0},
            {0, 0, 1, 1, 1, 1, 1, 1, 0, 0},
            {0, 0, 1, 1, 1, 1, 1, 1, 0, 0},
            {0, 0, 1, 1, 1, 1, 1, 1, 0, 0},
            {0, 0, 1, 1, 1, 1, 1, 1, 0, 0},
        };

        System.out.println("brightestSquare() Test " + testNum++);
        got = prj.brightestSquare(image, 1);
        expected = 3;
        test.printResult(got, expected);

        System.out.println("brightestSquare() Test " + testNum++);
        got = prj.brightestSquare(image, 2);
        expected = 11;
        test.printResult(got, expected);

        System.out.println("brightestSquare() Test " + testNum++);
        got = prj.brightestSquare(image, 3);
        expected = 19;
        test.printResult(got, expected);

        System.out.println("brightestSquare() Test " + testNum++);
        got = prj.brightestSquare(image, 4);
        expected = 28;
        test.printResult(got, expected);

        System.out.println("brightestSquare() Test " + testNum++);
        got = prj.brightestSquare(largeImage, 6);
        expected = 37;
        test.printResult(got, expected);

        System.out.println("brightestSquare() Test " + testNum++);
        got = prj.brightestSquare(largeImage, 1);
        expected = 2;
        test.printResult(got, expected);

        // darkestPath()
        int[][] largeImage2 = new int[][] {
            {0, 0, 3, 3, 3, 3, 3, 3, 3, 3},
            {3, 0, 0, 3, 3, 3, 3, 3, 3, 3},
            {3, 3, 0, 0, 3, 3, 3, 3, 3, 3},
            {3, 3, 3, 0, 0, 3, 0, 0, 0, 3},
            {3, 3, 3, 3, 0, 0, 0, 3, 0, 0},
            {3, 3, 3, 3, 3, 3, 3, 3, 0, 69}

        };
        System.out.println("darkestPath() Test " + testNum++);
        got = prj.darkestPath(image, 0, 0, 3, 3);
        expected = 3;
        test.printResult(got, expected);

        System.out.println("darkestPath() Test " + testNum++);
        got = prj.darkestPath(image, 0, 0, 2, 0);
        expected = 1;
        test.printResult(got, expected);

        System.out.println("darkestPath() Test " + testNum++);
        got = prj.darkestPath(largeImage2, 0, 0, 5, 9);
        expected = 69;
        test.printResult(got, expected);

        System.out.println("darkestPath() Test " + testNum++);
        got = prj.darkestPath(largeImage2, 0, 0, 5, 8);
        expected = 0;
        test.printResult(got, expected);



        System.out.println(test.passed + "/" + (testNum-1) + " tests passed.");
    }
}