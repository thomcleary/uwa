import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue; 
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import java.util.ArrayList;

/**
 * This class provides unit test cases for the Round class.
 * @author Lyndon While
 * @version 1.0
 */
public class RoundTest
{
    private Round r1;
    private Match m1, m2, m3;
    private ArrayList<String> ts;

    /**
     * Sets up the test fixture.
     *
     * Called before every test case method.
     */
    @Before
    public void setUp()
    {
        r1 = new Round();
        m1 = new Match("t1h", "t1a");
        m2 = new Match("t2h", "t2a");
        m3 = new Match("t3h", "t3a");
        ts = new ArrayList<>();
    }

    private String error(int k, String m)
    {
        return "error " + k + " in " + m + " -";
    }

    @Test
    public void testconstructor() 
    {
        String m = "constructor";
        assertTrue  (error(1,m),    r1.getMatches() != null);
        assertEquals(error(2,m), 0, r1.getMatches().size()); 
    }

    @Test
    public void testaddMatch() 
    {
        String m = "addMatch";
        ArrayList<Match> r1m = r1.getMatches();
        
        r1.addMatch(m1);
        assertEquals(error(1,m), 1,  r1m.size());
        assertEquals(error(2,m), m1, r1m.get(0));
        
        r1.addMatch(m2);
        assertEquals(error(3,m), 2,  r1m.size());
        assertEquals(error(4,m), m1, r1m.get(0));
        assertEquals(error(5,m), m2, r1m.get(1));
    }

    @Test
    public void testdeleteMatch() 
    {
        String m = "deleteMatch";
        ArrayList<Match> r1m = r1.getMatches();
        
        r1.deleteMatch(0);
        assertEquals(error(1,m),  0,  r1m.size());
        
        r1.addMatch(m1); r1.addMatch(m2); r1.addMatch(m3);
        assertEquals(error(2,m),  3,  r1m.size());
        assertEquals(error(3,m),  m1, r1m.get(0));
        assertEquals(error(4,m),  m2, r1m.get(1));
        assertEquals(error(5,m),  m3, r1m.get(2));
        
        r1.deleteMatch(1);
        assertEquals(error(6,m),  2,  r1m.size());
        assertEquals(error(7,m),  m1, r1m.get(0));
        assertEquals(error(8,m),  m3, r1m.get(1));
        
        r1.deleteMatch(1);
        assertEquals(error(9,m),  1,  r1m.size());
        assertEquals(error(10,m), m1, r1m.get(0));
        
        r1.deleteMatch(1);
        assertEquals(error(11,m), 1,  r1m.size());
        assertEquals(error(12,m), m1, r1m.get(0));
        
        r1.deleteMatch(0);
        assertEquals(error(13,m), 0,  r1m.size());
    }

    @Test
    public void testmakeRound() 
    {
        String m = "makeRound";
        ArrayList<Match> r1m;
        
        ts.add("t1"); ts.add("t2"); // 12
        r1.makeRound(ts, true);
        r1m = r1.getMatches();
        assertEquals(error(1,m), 1,    r1m.size());
        assertEquals(error(2,m), "t1", r1m.get(0).getHome());
        assertEquals(error(3,m), "t2", r1m.get(0).getAway());
        
        assertEquals(error(31,m), 2,    ts.size()); // ts can't be changed at the end
        assertEquals(error(32,m), "t1", ts.get(0));
        assertEquals(error(33,m), "t2", ts.get(1));
        
        ts.add("t3"); ts.add("t4"); ts.add(0, "t5"); ts.add(1, "t6"); // 561234
        r1.makeRound(ts, false);
        r1m = r1.getMatches();
        assertEquals(error(4,m),  3,    r1m.size());
        assertEquals(error(5,m),  "t6", r1m.get(0).getHome());
        assertEquals(error(6,m),  "t5", r1m.get(0).getAway());
        assertEquals(error(7,m),  "t1", r1m.get(1).getHome());
        assertEquals(error(8,m),  "t4", r1m.get(1).getAway());
        assertEquals(error(9,m),  "t2", r1m.get(2).getHome());
        assertEquals(error(10,m), "t3", r1m.get(2).getAway());
        
        assertEquals(error(91,m), 6,    ts.size()); // ts can't be changed at the end
        assertEquals(error(92,m), "t5", ts.get(0));
        assertEquals(error(93,m), "t6", ts.get(1));
        assertEquals(error(94,m), "t1", ts.get(2));
        assertEquals(error(95,m), "t2", ts.get(3));
        assertEquals(error(96,m), "t3", ts.get(4));
        assertEquals(error(97,m), "t4", ts.get(5));
    }

    @Test
    public void testgetDisplayValue() 
    {
        String m = "getDisplayValue";
        // using trim allows any whitespace at the ends 
        r1.addMatch(m1);
        assertEquals(error(1,m), "t1h vs. t1a",                           r1.getDisplayValue().trim());
        r1.addMatch(m2);
        assertEquals(error(2,m), "t1h vs. t1a\nt2h vs. t2a",              r1.getDisplayValue().trim());
        r1.addMatch(m3);
        assertEquals(error(3,m), "t1h vs. t1a\nt2h vs. t2a\nt3h vs. t3a", r1.getDisplayValue().trim());
    }
}
