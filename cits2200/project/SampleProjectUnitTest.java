/**
 * @author Andrew "Gozz" Gozzard <andrew.gozzard@uwa.edu.au>
 *
 * A sample unit tester for the 2020 CITS2200 Project.
 *
 * DO NOT modify this file in the course of completing your project.
 * You are, however, encouraged to copy it and use it to construct your own tests.
 */
public class SampleProjectUnitTest {
    /**
     * Total number of tests run
     */
    private static int numTest = 0;

    /**
     * Total number of tests passed
     */
    private static int numPass = 0;

    /**
     * Helper function to print out a test result nicely and update counters
     * @param name The name of the test to display as output
     * @param pass Whether or note the test passed
     */
    private static void test(String name, boolean pass) {
        numTest++;
        if (pass) {
            numPass++;
            System.out.print("Pass:");
        } else {
            System.out.print("FAIL:");
        }
        System.out.print("\t");
        System.out.println(name);
    }

    private static void testInts(String name, int actual, int expected) {
        boolean pass = actual == expected;
        test(name, pass);
        if (!pass) {
            System.out.println("\tExpected " + expected + " got " + actual);
        }
    }

    public static void floodFillCountTest() {
        Project proj = new MyProject();

        int[][] image = new int[][] {
            { 0, 0, 1, 1, 1 },
            { 0, 1, 1, 2, 2 },
            { 2, 3, 3, 0, 2 },
            { 2, 2, 2, 2, 2 },
        };

        String pref = "floodFillCount: ";

        testInts(pref + "already black", 
            proj.floodFillCount(image, 0, 1), 0);

        testInts(pref + "example 1", 
            proj.floodFillCount(image, 1, 2), 5);

        testInts(pref + "example 2", 
            proj.floodFillCount(image, 2, 0), 9);

        testInts(pref + "example 3", 
            proj.floodFillCount(image, 2, 1), 2);
    }

    public static void brightestSquareTest() {
        Project proj = new MyProject();

        int[][] image = new int[][] {
            { 0, 0, 1, 1, 1 },
            { 0, 1, 1, 2, 2 },
            { 2, 3, 3, 0, 2 },
            { 2, 2, 2, 2, 2 }
        };

        String pref = "brightestSquare: ";

        testInts(pref + "k = 1", 
            proj.brightestSquare(image, 1), 3);

        testInts(pref + "k = 2", 
            proj.brightestSquare(image, 2), 10);

        testInts(pref + "k = 3", 
            proj.brightestSquare(image, 3), 16);

        testInts(pref + "k = 4", 
            proj.brightestSquare(image, 4), 25);
    }

    public static void darkestPathTest() {
        Project proj = new MyProject();

        int[][] image = new int[][] {
            { 0, 0, 1, 1, 1 },
            { 0, 1, 1, 2, 2 },
            { 2, 3, 3, 0, 2 },
            { 2, 2, 2, 2, 2 },
        };

        String pref = "darkestPath: ";

        testInts(pref + "example 1", 
            proj.darkestPath(image, 1, 0, 2, 3), 2);

        testInts(pref + "example 2", 
            proj.darkestPath(image, 1, 0, 0, 4), 1);

        testInts(pref + "example 3", 
            proj.darkestPath(image, 1, 0, 0, 1), 0);
    }

    public static void brightestPixelsInRowSegmentsTest() {
        Project proj = new MyProject();

        int[][] image = new int[][] {
            { 0, 1, 2, 3, 3, 2, 1, 0, 1 },
            { 9, 4, 7, 4, 6, 8, 3, 6, 1 },
        };

        int[][] queries = new int[][] {
            { 0, 2, 3 },
            { 0, 1, 4 },
            { 1, 0, 3 },
            { 1, 3, 5 },
        };

        int[] results = proj.brightestPixelsInRowSegments(image, queries);

        String pref = "brightestPixelsInRowSegments: ";

        testInts(pref + "example 1", results[0], 2);
        testInts(pref + "example 2", results[1], 3);
        testInts(pref + "example 3", results[2], 9);
        testInts(pref + "example 4", results[3], 6);

        // Test edge conditions by counting up through range sizes
        image = new int[][] {
            { 1, 2, 3, 4, 5, 6, 7, 8, 9 },
        };

        queries = new int[][] {
            { 0, 1, 2 },
            { 0, 1, 3 },
            { 0, 1, 4 },
            { 0, 1, 5 },
            { 0, 1, 6 },
            { 0, 1, 7 },
            { 0, 1, 8 },
            { 0, 1, 9 },
        };

        results = proj.brightestPixelsInRowSegments(image, queries);

        pref = pref + "counting";

        testInts(pref, results[0], 2);
        testInts(pref, results[1], 3);
        testInts(pref, results[2], 4);
        testInts(pref, results[3], 5);
        testInts(pref, results[4], 6);
        testInts(pref, results[5], 7);
        testInts(pref, results[6], 8);
        testInts(pref, results[7], 9);
    }

    public static void printSummary() {
        System.out.println();
        System.out.println(
            "Passed " +
            Integer.toString(numPass) +
            "/" +
            Integer.toString(numTest) +
            " tests");
        if (numPass == numTest) {
            System.out.println("All tests passed");
        } else {
            System.out.println(Integer.toString(numTest-numPass) + " TESTS FAILED");
        }
    }

    public static void main(String[] args) {
        floodFillCountTest();
        brightestSquareTest();
        darkestPathTest();
        brightestPixelsInRowSegmentsTest();

        printSummary();
    }
}