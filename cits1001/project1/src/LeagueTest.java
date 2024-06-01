import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import java.util.ArrayList;

/**
 * This class provides unit test cases for the League class.
 * @author Lyndon While
 * @version 1.0
 */
public class LeagueTest
{
    private League l2, l3, l4, lf;

    /**
     * Sets up the test fixture.
     *
     * Called before every test case method.
     */
    @Before
    public void setUp()
    {
        l2 = new League(2);
        l3 = new League(3);
        l4 = new League(4);
        lf = new League("towns.txt");
    }
    
    private String error(int k, String m)
    {
        return "error " + k + " in " + m + " -";
    }

    @Test
    public void testconstructor1() 
    {
        String m = "constructor1";
        
        ArrayList<String> ts = l4.getTeams();
        assertTrue  (error(1,m),       ts != null);
        assertEquals(error(2,m), 4,    ts.size());
        assertEquals(error(3,m), "T1", ts.get(0));
        assertEquals(error(4,m), "T2", ts.get(1));
        assertEquals(error(5,m), "T3", ts.get(2));
        assertEquals(error(6,m), "T4", ts.get(3));
        assertTrue  (error(7,m),       l4.getFixtures() != null);
        assertEquals(error(8,m), 0,    l4.getFixtures().size());
    }
    
    @Test
    public void testaddRound()
    {
        String m = "addRound";
        ArrayList<Round> fs = l2.getFixtures();
        assertEquals(error(1,m),  0,  fs.size());
        Round r0 = new Round();
        l2.addRound(r0);
        assertEquals(error(2,m),  1,  fs.size());
        assertEquals(error(3,m),  r0, fs.get(0));
        Round r1 = new Round();
        l2.addRound(r1);
        assertEquals(error(4,m),  2,  fs.size());
        assertEquals(error(5,m),  r0, fs.get(0));
        assertEquals(error(6,m),  r1, fs.get(1));
        Round r2 = new Round();
        l2.addRound(r2);
        assertEquals(error(7,m),  3,  fs.size());
        assertEquals(error(8,m),  r0, fs.get(0));
        assertEquals(error(9,m),  r1, fs.get(1));
        assertEquals(error(10,m), r2, fs.get(2));
    }
    
    @Test
    public void testrotateTeams() 
    {
        String m = "rotateTeams";
        ArrayList<String> ts;
        
        l4.rotateTeams();
        ts = l4.getTeams();
        assertEquals(error(1,m), 4,    ts.size());
        assertEquals(error(2,m), "T1", ts.get(0));
        assertEquals(error(3,m), "T4", ts.get(1));
        assertEquals(error(4,m), "T2", ts.get(2));
        assertEquals(error(5,m), "T3", ts.get(3));
        assertEquals(error(6,m), 0,    l4.getFixtures().size());
        
        l2.rotateTeams();
        ts = l2.getTeams();
        assertEquals(error(7,m), 2,    ts.size());
        assertEquals(error(8,m), "T1", ts.get(0));
        assertEquals(error(9,m), "T2", ts.get(1));
        assertEquals(error(10,m), 0,   l2.getFixtures().size());
    }
    
    @Test
    public void testmakeEvenSchedule() 
    {
        String m = "makeEvenSchedule";
        ArrayList<Round> fs;
        ArrayList<Match> r;
        ArrayList<String> ts;
        
        l4.makeEvenSchedule();
        fs = l4.getFixtures();
        assertEquals(error(21,m), 3,    fs.size());
        r = fs.get(0).getMatches();
        assertEquals(error(22,m), 2,    r.size());
        assertEquals(error(23,m), "T1", r.get(0).getHome());
        assertEquals(error(24,m), "T2", r.get(0).getAway());
        assertEquals(error(25,m), "T3", r.get(1).getHome());
        assertEquals(error(26,m), "T4", r.get(1).getAway());
        r = fs.get(1).getMatches();
        assertEquals(error(27,m), 2,    r.size());
        assertEquals(error(28,m), "T4", r.get(0).getHome());
        assertEquals(error(29,m), "T1", r.get(0).getAway());
        assertEquals(error(30,m), "T2", r.get(1).getHome());
        assertEquals(error(31,m), "T3", r.get(1).getAway());
        r = fs.get(2).getMatches();
        assertEquals(error(32,m), 2,    r.size());
        assertEquals(error(33,m), "T1", r.get(0).getHome());
        assertEquals(error(34,m), "T3", r.get(0).getAway());
        assertEquals(error(35,m), "T4", r.get(1).getHome());
        assertEquals(error(36,m), "T2", r.get(1).getAway());
        ts = l4.getTeams();
        assertEquals(error(37,m), 4,    ts.size());
        assertEquals(error(38,m), "T1", ts.get(0));
        assertEquals(error(39,m), "T2", ts.get(1));
        assertEquals(error(40,m), "T3", ts.get(2));
        assertEquals(error(41,m), "T4", ts.get(3));
    }
    
    @Test
    public void testmakeSchedule() 
    {
        String m = "makeSchedule";
        ArrayList<Round> fs;
        ArrayList<Match> r;
        ArrayList<String> ts;
        
        l3.makeSchedule();
        fs = l3.getFixtures();
        assertEquals(error(1,m),  3,    fs.size());
        r = fs.get(0).getMatches();
        assertEquals(error(2,m),  1,    r.size());
        assertEquals(error(3,m),  "T2", r.get(0).getHome());
        assertEquals(error(4,m),  "T3", r.get(0).getAway());
        r = fs.get(1).getMatches();
        assertEquals(error(5,m),  1,    r.size());
        assertEquals(error(6,m),  "T1", r.get(0).getHome());
        assertEquals(error(7,m),  "T2", r.get(0).getAway());
        r = fs.get(2).getMatches();
        assertEquals(error(8,m),  1,    r.size());
        assertEquals(error(9,m),  "T3", r.get(0).getHome());
        assertEquals(error(10,m), "T1", r.get(0).getAway());
        ts = l3.getTeams();
        assertEquals(error(11,m), 3,    ts.size());
        assertEquals(error(12,m), "T1", ts.get(0));
        assertEquals(error(13,m), "T2", ts.get(1));
        assertEquals(error(14,m), "T3", ts.get(2));
        
        l4.makeSchedule();
        fs = l4.getFixtures();
        assertEquals(error(21,m), 3,    fs.size());
        r = fs.get(0).getMatches();
        assertEquals(error(22,m), 2,    r.size());
        assertEquals(error(23,m), "T1", r.get(0).getHome());
        assertEquals(error(24,m), "T2", r.get(0).getAway());
        assertEquals(error(25,m), "T3", r.get(1).getHome());
        assertEquals(error(26,m), "T4", r.get(1).getAway());
        r = fs.get(1).getMatches();
        assertEquals(error(27,m), 2,    r.size());
        assertEquals(error(28,m), "T4", r.get(0).getHome());
        assertEquals(error(29,m), "T1", r.get(0).getAway());
        assertEquals(error(30,m), "T2", r.get(1).getHome());
        assertEquals(error(31,m), "T3", r.get(1).getAway());
        r = fs.get(2).getMatches();
        assertEquals(error(32,m), 2,    r.size());
        assertEquals(error(33,m), "T1", r.get(0).getHome());
        assertEquals(error(34,m), "T3", r.get(0).getAway());
        assertEquals(error(35,m), "T4", r.get(1).getHome());
        assertEquals(error(36,m), "T2", r.get(1).getAway());
        ts = l4.getTeams();
        assertEquals(error(37,m), 4,    ts.size());
        assertEquals(error(38,m), "T1", ts.get(0));
        assertEquals(error(39,m), "T2", ts.get(1));
        assertEquals(error(40,m), "T3", ts.get(2));
        assertEquals(error(41,m), "T4", ts.get(3));
    }
    
    @Test
    public void testgetDisplayValue() 
    {
        String m = "getDisplayValue";
        // using trim allows any whitespace at the ends 
        Round r1 = new Round();
        r1.addMatch(new Match("T1", "T2")); r1.addMatch(new Match("T3", "T4")); 
        Round r2 = new Round();
        r2.addMatch(new Match("T4", "T1")); r2.addMatch(new Match("T2", "T3")); 
        Round r3 = new Round();
        r3.addMatch(new Match("T1", "T3")); r3.addMatch(new Match("T4", "T2")); 
        l4.addRound(r1); l4.addRound(r2); l4.addRound(r3); 
        // l4.makeSchedule();
        assertEquals(error(1,m), "Round 1\nT1 vs. T2\nT3 vs. T4\n\n" + 
                                 "Round 2\nT4 vs. T1\nT2 vs. T3\n\n" + 
                                 "Round 3\nT1 vs. T3\nT4 vs. T2",
                     l4.getDisplayValue().trim()); 
    }

    @Test
    public void testconstructor2() 
    {
        String m = "constructor2";
        ArrayList<String> ts = lf.getTeams();
        assertTrue  (error(1,m),                  ts != null);
        assertEquals(error(2,m), 5,               ts.size());
        assertEquals(error(3,m), "Wonglepong",    ts.get(0));
        assertEquals(error(4,m), "Waipu",         ts.get(1));
        assertEquals(error(5,m), "Great Snoring", ts.get(2));
        assertEquals(error(6,m), "Pwllheli",      ts.get(3));
        assertEquals(error(7,m), "Two Egg",       ts.get(4));
        assertTrue  (error(8,m),                  lf.getFixtures() != null);
        assertEquals(error(9,m), 0,               lf.getFixtures().size());
    }
}
