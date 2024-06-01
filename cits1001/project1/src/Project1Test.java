import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import java.util.ArrayList;

/**
 * This class provides unit test cases for Project 1 in 2019 Sem. 1. 
 * @author Lyndon While
 * @version 1.0
 */
public class Project1Test
{
    private ArrayList<String> ts;
    private Match[]  ms;
    private Round[]  rs;
    private League[] ls;
    League planets;

    /**
     * Sets up the test fixture.
     *
     * Called before every test case method.
     */
    @Before
    public void setUp()
    {
        ts = new ArrayList<>();
        ms = new Match[4];
        for (int k = 0; k < ms.length; k++)
            ms[k] = new Match("tH" + k, "tA" + k);
        rs = new Round[10];
        for (int k = 0; k < rs.length; k++)
            rs[k] = new Round();
        ls = new League[11];
        for (int k = 0; k < ls.length; k++)
            ls[k] = new League(k);
        planets = new League("planets.txt");
    }

    private String error(int k, String m)
    {
        return "error " + k + " in " + m + " -";
    }

    @Test
    public void testgetHome() 
    {
        assertEquals(error(1,"getHome"), "tH1", ms[1].getHome());
    }

    @Test
    public void testgetAway() 
    {
        assertEquals(error(1,"getAway"), "tA2", ms[2].getAway());
    }

    @Test
    public void testMatchgetDisplayValue() 
    {
        assertTrue(error(1,"Match getDisplayValue"), ms[3].getDisplayValue().equals("tH3 vs. tA3"));
    }

    @Test
    public void testRoundconstructor() 
    {
        String m = "constructor";
        assertTrue  (error(1,m),    rs[0].getMatches() != null);
        assertEquals(error(2,m), 0, rs[0].getMatches().size()); 
    }

    @Test
    public void testaddMatch() 
    {
        String m = "addMatch";
        ArrayList<Match> r1m = rs[1].getMatches();        
        for (int k = 0; k < 10; k++) // add one Match in each iteration, check size and all items
        {
            rs[1].addMatch(ms[k % 4]);
            assertEquals(error(1,m), k+1, r1m.size());
            for (int j = 0; j <= k; j++)
                assertEquals(error(2,m), ms[j % 4], r1m.get(j));
        }
    }

    @Test
    public void testdeleteMatch() 
    {
        String m = "deleteMatch";
        ArrayList<Match> r1m = rs[1].getMatches();
        
        rs[1].deleteMatch(0); // failed delete
        assertEquals(error(1,m), 0, r1m.size());
        
        for (int k = 0; k < 4; k++) // add four matches 
            rs[1].addMatch(ms[k]); 
        assertEquals(error(2,m), 4, r1m.size());
        for (int k = 0; k < 4; k++)
            assertEquals(error(3,m), ms[k], r1m.get(k));
        
        for (int z = 4; z < 10; z++)
        {
            rs[1].deleteMatch(z); // failed deletes
            assertEquals(error(4,m), 4, r1m.size());
            for (int k = 0; k < 4; k++)
                assertEquals(error(5,m), ms[k], r1m.get(k));
        }
        
        rs[1].deleteMatch(0); // delete first item 123 left
        assertEquals(error(6,m), 3, r1m.size());
        for (int k = 0; k < 3; k++)
            assertEquals(error(7,m), ms[k+1], r1m.get(k));
        
        for (int z = -9; z < 0; z++)
        {
            rs[1].deleteMatch(z); // failed deletes
            assertEquals(error(8,m), 3, r1m.size());
            for (int k = 0; k < 3; k++)
                assertEquals(error(9,m), ms[k+1], r1m.get(k));
        }
        
        rs[1].deleteMatch(1); // delete from middle 13 left
        assertEquals(error(10,m), 2, r1m.size());
        for (int k = 0; k < 2; k++)
            assertEquals(error(11,m), ms[2*k+1], r1m.get(k));
        
        rs[1].deleteMatch(1); // delete last item 1 left
        assertEquals(error(12,m), 1,     r1m.size());
        assertEquals(error(13,m), ms[1], r1m.get(0));
        
        rs[1].deleteMatch(1); // failed delete
        assertEquals(error(14,m), 1,     r1m.size());
        assertEquals(error(15,m), ms[1], r1m.get(0));
        
        rs[1].deleteMatch(0); // delete only item
        assertEquals(error(16,m), 0,     r1m.size());
    }
    
    @Test
    public void testmakeRound()
    {
        String m = "makeRound";
        ArrayList<Match> r1m;
        
        ts.add("t11"); ts.add("t12"); // 12
        rs[1].makeRound(ts, true);
        r1m = rs[1].getMatches();
        assertEquals(error(1,m), 1,     r1m.size());
        assertEquals(error(2,m), "t11", r1m.get(0).getHome());
        assertEquals(error(3,m), "t12", r1m.get(0).getAway());
        
        assertEquals(error(31,m), 2,     ts.size()); // ts can't be changed
        assertEquals(error(32,m), "t11", ts.get(0));
        assertEquals(error(33,m), "t12", ts.get(1));
        
        ts.add("t13"); ts.add("t14"); // 1234
        rs[1].makeRound(ts, false);
        r1m = rs[1].getMatches();
        assertEquals(error(4,m),  2,     r1m.size());
        assertEquals(error(5,m),  "t12", r1m.get(0).getHome());
        assertEquals(error(6,m),  "t11", r1m.get(0).getAway());
        assertEquals(error(7,m),  "t13", r1m.get(1).getHome());
        assertEquals(error(8,m),  "t14", r1m.get(1).getAway());
        
        assertEquals(error(81,m), 4,     ts.size()); // ts can't be changed
        assertEquals(error(82,m), "t11", ts.get(0));
        assertEquals(error(83,m), "t12", ts.get(1));
        assertEquals(error(84,m), "t13", ts.get(2));
        assertEquals(error(85,m), "t14", ts.get(3));
        
        ts.add(0, "t15"); ts.add(1, "t16"); // 561234
        rs[1].makeRound(ts, true);
        r1m = rs[1].getMatches();
        assertEquals(error(29,m), 3,     r1m.size());
        assertEquals(error(20,m), "t15", r1m.get(0).getHome());
        assertEquals(error(21,m), "t16", r1m.get(0).getAway());
        assertEquals(error(22,m), "t11", r1m.get(1).getHome());
        assertEquals(error(23,m), "t14", r1m.get(1).getAway());
        assertEquals(error(24,m), "t12", r1m.get(2).getHome());
        assertEquals(error(25,m), "t13", r1m.get(2).getAway());
        
        assertEquals(error(51,m), 6,     ts.size()); // ts can't be changed
        assertEquals(error(52,m), "t15", ts.get(0));
        assertEquals(error(53,m), "t16", ts.get(1));
        assertEquals(error(54,m), "t11", ts.get(2));
        assertEquals(error(55,m), "t12", ts.get(3));
        assertEquals(error(56,m), "t13", ts.get(4));
        assertEquals(error(57,m), "t14", ts.get(5));
        
        ts.add("t17"); ts.add("t18"); // 56123478
        rs[1].makeRound(ts, false);
        r1m = rs[1].getMatches();
        assertEquals(error(9,m),  4,     r1m.size());
        assertEquals(error(10,m), "t16", r1m.get(0).getHome());
        assertEquals(error(11,m), "t15", r1m.get(0).getAway());
        assertEquals(error(12,m), "t11", r1m.get(1).getHome());
        assertEquals(error(13,m), "t18", r1m.get(1).getAway());
        assertEquals(error(14,m), "t12", r1m.get(2).getHome());
        assertEquals(error(15,m), "t17", r1m.get(2).getAway());
        assertEquals(error(16,m), "t13", r1m.get(3).getHome());
        assertEquals(error(17,m), "t14", r1m.get(3).getAway());
        
        assertEquals(error(91,m), 8,     ts.size()); // ts can't be changed
        assertEquals(error(92,m), "t15", ts.get(0));
        assertEquals(error(93,m), "t16", ts.get(1));
        assertEquals(error(94,m), "t11", ts.get(2));
        assertEquals(error(95,m), "t12", ts.get(3));
        assertEquals(error(96,m), "t13", ts.get(4));
        assertEquals(error(97,m), "t14", ts.get(5));
        assertEquals(error(98,m), "t17", ts.get(6));
        assertEquals(error(99,m), "t18", ts.get(7));
    }

    @Test
    public void testRoundgetDisplayValue() 
    {
        String m = "Round getDisplayValue";
        // using trim allows any whitespace at the ends 
        rs[1].addMatch(ms[1]);
        assertTrue(error(1,m), rs[1].getDisplayValue().trim().equals("tH1 vs. tA1"));
        rs[1].addMatch(ms[2]);
        assertTrue(error(2,m), rs[1].getDisplayValue().trim().equals("tH1 vs. tA1\ntH2 vs. tA2"));
        rs[1].addMatch(ms[3]);
        assertTrue(error(3,m), rs[1].getDisplayValue().trim().equals("tH1 vs. tA1\ntH2 vs. tA2\ntH3 vs. tA3"));
        rs[1].addMatch(ms[0]);
        assertTrue(error(4,m), rs[1].getDisplayValue().trim().equals("tH1 vs. tA1\ntH2 vs. tA2\ntH3 vs. tA3\ntH0 vs. tA0"));
    }
    
    @Test
    public void testLeagueconstructor1() 
    {
        String m = "constructor1";
        for (int k = 0; k < ls.length; k++)
        {
            ts = ls[k].getTeams();
            assertTrue  (error(1,m),    ts != null);
            assertEquals(error(2,m), k, ts.size());
            for (int j = 1; j <= k; j++)
                assertEquals(error(3,m), "T" + j, ts.get(j - 1));
            assertTrue  (error(4,m),    ls[k].getFixtures() != null);
            assertEquals(error(5,m), 0, ls[k].getFixtures().size());
        }
    }
    
    @Test
    public void testaddRound()
    {
        String m = "addRound";
        ArrayList<Round> fs = ls[2].getFixtures();
        assertEquals(error(1,m),  0,  fs.size());
        for (int k = 0; k < rs.length; k++)
        {
            ls[2].addRound(rs[k]);
            assertEquals(error(2,m), k+1, fs.size());
            for (int j = 0; j <= k; j++)
                assertEquals(error(3,m), rs[j], fs.get(j));
        }
    }
    
    @Test
    public void testrotateTeams() 
    {
        String m = "rotateTeams more";
        for (int k = 2; k < ls.length; k ++)
        {
            ts = ls[k].getTeams();
            for (int q = 1; q < k; q++) // k-1 rotations takes us back to the start
            {
                ls[k].rotateTeams();
                assertEquals(error(1,m), k,    ts.size()); 
                assertEquals(error(2,m), "T1", ts.get(0));              // the first team is never changed
                for (int p = 1; p < q+1; p++)
                    assertEquals(error(3,m), "T" + (k-q+p), ts.get(p)); // then there are q teams from the end
                for (int j = q+1; j < k; j++)
                    assertEquals(error(4,m), "T" + (j-q+1), ts.get(j)); // then the other teams, moved along
                assertEquals(error(5,m), 0, ls[k].getFixtures().size());
            }
        }
    }
    
    // used for both makeEvenSchedule and makeSchedule
    private void testevenSchedules(String m)
    {
        ArrayList<Round> fs;
        ArrayList<Match> r;
        
        ls[2].makeEvenSchedule();
        fs = ls[2].getFixtures();
        assertEquals(error(1,m), 1,    fs.size());
        r = fs.get(0).getMatches();
        assertEquals(error(2,m), 1,    r.size());
        assertEquals(error(3,m), "T1", r.get(0).getHome());
        assertEquals(error(4,m), "T2", r.get(0).getAway());
        ts = ls[2].getTeams();
        assertEquals(error(5,m), 2,    ts.size());
        for (int k = 0; k < 2; k++)
            assertEquals(error(6,m), "T" + (k+1), ts.get(k));
        
        ls[4].makeEvenSchedule();
        fs = ls[4].getFixtures();
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
        ts = ls[4].getTeams();
        assertEquals(error(37,m), 4,    ts.size());
        for (int k = 0; k < 4; k++)
            assertEquals(error(38,m), "T" + (k+1), ts.get(k));
        
        ls[6].makeEvenSchedule();
        fs = ls[6].getFixtures();
        assertEquals(error(41,m), 5,    fs.size());
        r = fs.get(0).getMatches();
        assertEquals(error(42,m), 3,    r.size());
        assertEquals(error(43,m), "T1", r.get(0).getHome());
        assertEquals(error(44,m), "T2", r.get(0).getAway());
        assertEquals(error(45,m), "T3", r.get(1).getHome());
        assertEquals(error(46,m), "T6", r.get(1).getAway());
        assertEquals(error(45,m), "T4", r.get(2).getHome());
        assertEquals(error(46,m), "T5", r.get(2).getAway());
        r = fs.get(1).getMatches();
        assertEquals(error(47,m), 3,    r.size());
        assertEquals(error(48,m), "T6", r.get(0).getHome());
        assertEquals(error(49,m), "T1", r.get(0).getAway());
        assertEquals(error(50,m), "T2", r.get(1).getHome());
        assertEquals(error(51,m), "T5", r.get(1).getAway());
        assertEquals(error(52,m), "T3", r.get(2).getHome());
        assertEquals(error(53,m), "T4", r.get(2).getAway());
        r = fs.get(2).getMatches();
        assertEquals(error(54,m), 3,    r.size());
        assertEquals(error(55,m), "T1", r.get(0).getHome());
        assertEquals(error(56,m), "T5", r.get(0).getAway());
        assertEquals(error(57,m), "T6", r.get(1).getHome());
        assertEquals(error(58,m), "T4", r.get(1).getAway());
        assertEquals(error(59,m), "T2", r.get(2).getHome());
        assertEquals(error(60,m), "T3", r.get(2).getAway());
        r = fs.get(3).getMatches();
        assertEquals(error(61,m), 3,    r.size());
        assertEquals(error(62,m), "T4", r.get(0).getHome());
        assertEquals(error(63,m), "T1", r.get(0).getAway());
        assertEquals(error(64,m), "T5", r.get(1).getHome());
        assertEquals(error(65,m), "T3", r.get(1).getAway());
        assertEquals(error(66,m), "T6", r.get(2).getHome());
        assertEquals(error(67,m), "T2", r.get(2).getAway());
        r = fs.get(4).getMatches();
        assertEquals(error(68,m), 3,    r.size());
        assertEquals(error(69,m), "T1", r.get(0).getHome());
        assertEquals(error(70,m), "T3", r.get(0).getAway());
        assertEquals(error(71,m), "T4", r.get(1).getHome());
        assertEquals(error(72,m), "T2", r.get(1).getAway());
        assertEquals(error(73,m), "T5", r.get(2).getHome());
        assertEquals(error(74,m), "T6", r.get(2).getAway());
        ts = ls[6].getTeams();
        assertEquals(error(75,m), 6,    ts.size());
        for (int k = 0; k < 6; k++)
            assertEquals(error(76,m), "T" + (k+1), ts.get(k));
        
        ls[8].makeEvenSchedule();
        fs = ls[8].getFixtures();
        assertEquals(error(101,m), 7,    fs.size());
        r = fs.get(0).getMatches();
        assertEquals(error(102,m), 4,    r.size());
        assertEquals(error(103,m), "T1", r.get(0).getHome());
        assertEquals(error(104,m), "T2", r.get(0).getAway());
        assertEquals(error(105,m), "T3", r.get(1).getHome());
        assertEquals(error(106,m), "T8", r.get(1).getAway());
        assertEquals(error(107,m), "T4", r.get(2).getHome());
        assertEquals(error(108,m), "T7", r.get(2).getAway());
        assertEquals(error(109,m), "T5", r.get(3).getHome());
        assertEquals(error(110,m), "T6", r.get(3).getAway());
        r = fs.get(1).getMatches();
        assertEquals(error(111,m), 4,    r.size());
        assertEquals(error(112,m), "T8", r.get(0).getHome());
        assertEquals(error(113,m), "T1", r.get(0).getAway());
        assertEquals(error(114,m), "T2", r.get(1).getHome());
        assertEquals(error(115,m), "T7", r.get(1).getAway());
        assertEquals(error(116,m), "T3", r.get(2).getHome());
        assertEquals(error(117,m), "T6", r.get(2).getAway());
        assertEquals(error(118,m), "T4", r.get(3).getHome());
        assertEquals(error(119,m), "T5", r.get(3).getAway());
        r = fs.get(2).getMatches();
        assertEquals(error(120,m), 4,    r.size());
        assertEquals(error(121,m), "T1", r.get(0).getHome());
        assertEquals(error(122,m), "T7", r.get(0).getAway());
        assertEquals(error(123,m), "T8", r.get(1).getHome());
        assertEquals(error(124,m), "T6", r.get(1).getAway());
        assertEquals(error(125,m), "T2", r.get(2).getHome());
        assertEquals(error(126,m), "T5", r.get(2).getAway());
        assertEquals(error(127,m), "T3", r.get(3).getHome());
        assertEquals(error(128,m), "T4", r.get(3).getAway());
        r = fs.get(3).getMatches();
        assertEquals(error(129,m), 4,    r.size());
        assertEquals(error(130,m), "T6", r.get(0).getHome());
        assertEquals(error(131,m), "T1", r.get(0).getAway());
        assertEquals(error(132,m), "T7", r.get(1).getHome());
        assertEquals(error(133,m), "T5", r.get(1).getAway());
        assertEquals(error(134,m), "T8", r.get(2).getHome());
        assertEquals(error(135,m), "T4", r.get(2).getAway());
        assertEquals(error(136,m), "T2", r.get(3).getHome());
        assertEquals(error(137,m), "T3", r.get(3).getAway());
        r = fs.get(4).getMatches();
        assertEquals(error(138,m), 4,    r.size());
        assertEquals(error(139,m), "T1", r.get(0).getHome());
        assertEquals(error(140,m), "T5", r.get(0).getAway());
        assertEquals(error(141,m), "T6", r.get(1).getHome());
        assertEquals(error(142,m), "T4", r.get(1).getAway());
        assertEquals(error(143,m), "T7", r.get(2).getHome());
        assertEquals(error(144,m), "T3", r.get(2).getAway());
        assertEquals(error(145,m), "T8", r.get(3).getHome());
        assertEquals(error(146,m), "T2", r.get(3).getAway());
        r = fs.get(5).getMatches();
        assertEquals(error(147,m), 4,    r.size());
        assertEquals(error(148,m), "T4", r.get(0).getHome());
        assertEquals(error(149,m), "T1", r.get(0).getAway());
        assertEquals(error(150,m), "T5", r.get(1).getHome());
        assertEquals(error(151,m), "T3", r.get(1).getAway());
        assertEquals(error(152,m), "T6", r.get(2).getHome());
        assertEquals(error(153,m), "T2", r.get(2).getAway());
        assertEquals(error(154,m), "T7", r.get(3).getHome());
        assertEquals(error(155,m), "T8", r.get(3).getAway());
        r = fs.get(6).getMatches();
        assertEquals(error(156,m), 4,    r.size());
        assertEquals(error(157,m), "T1", r.get(0).getHome());
        assertEquals(error(158,m), "T3", r.get(0).getAway());
        assertEquals(error(159,m), "T4", r.get(1).getHome());
        assertEquals(error(160,m), "T2", r.get(1).getAway());
        assertEquals(error(161,m), "T5", r.get(2).getHome());
        assertEquals(error(162,m), "T8", r.get(2).getAway());
        assertEquals(error(163,m), "T6", r.get(3).getHome());
        assertEquals(error(164,m), "T7", r.get(3).getAway());
        ts = ls[8].getTeams();
        assertEquals(error(165,m), 8,    ts.size());
        for (int k = 0; k < 8; k++)
            assertEquals(error(166,m), "T" + (k+1), ts.get(k));
    }
    
    @Test
    public void testmakeEvenSchedule() 
    {
        String m = "makeEvenSchedule";
        testevenSchedules(m);
    }
    
    @Test
    public void testmakeSchedule() 
    {
        String m = "makeSchedule";
        testevenSchedules(m);
        
        ArrayList<Round> fs;
        ArrayList<Match> r;
        
        ls[3].makeSchedule();
        fs = ls[3].getFixtures();
        assertEquals(error(301,m), 3,    fs.size());
        r = fs.get(0).getMatches();
        assertEquals(error(302,m), 1,    r.size());
        assertEquals(error(303,m), "T2", r.get(0).getHome());
        assertEquals(error(304,m), "T3", r.get(0).getAway());
        r = fs.get(1).getMatches();
        assertEquals(error(305,m), 1,    r.size());
        assertEquals(error(306,m), "T1", r.get(0).getHome());
        assertEquals(error(307,m), "T2", r.get(0).getAway());
        r = fs.get(2).getMatches();
        assertEquals(error(308,m), 1,    r.size());
        assertEquals(error(309,m), "T3", r.get(0).getHome());
        assertEquals(error(310,m), "T1", r.get(0).getAway());
        ts = ls[3].getTeams();
        assertEquals(error(311,m), 3,    ts.size());
        for (int k = 0; k < 3; k++)
            assertEquals(error(312,m), "T" + (k+1), ts.get(k));
        
        ls[5].makeSchedule();
        fs = ls[5].getFixtures();
        assertEquals(error(501,m), 5,    fs.size());
        r = fs.get(0).getMatches();
        assertEquals(error(502,m), 2,    r.size());
        assertEquals(error(503,m), "T2", r.get(0).getHome());
        assertEquals(error(504,m), "T5", r.get(0).getAway());
        assertEquals(error(505,m), "T3", r.get(1).getHome());
        assertEquals(error(506,m), "T4", r.get(1).getAway());
        r = fs.get(1).getMatches();
        assertEquals(error(507,m), 2,    r.size());
        assertEquals(error(508,m), "T1", r.get(0).getHome());
        assertEquals(error(509,m), "T4", r.get(0).getAway());
        assertEquals(error(510,m), "T2", r.get(1).getHome());
        assertEquals(error(511,m), "T3", r.get(1).getAway());
        r = fs.get(2).getMatches();
        assertEquals(error(512,m), 2,    r.size());
        assertEquals(error(513,m), "T5", r.get(0).getHome());
        assertEquals(error(514,m), "T3", r.get(0).getAway());
        assertEquals(error(515,m), "T1", r.get(1).getHome());
        assertEquals(error(516,m), "T2", r.get(1).getAway());
        r = fs.get(3).getMatches();
        assertEquals(error(517,m), 2,    r.size());
        assertEquals(error(518,m), "T4", r.get(0).getHome());
        assertEquals(error(519,m), "T2", r.get(0).getAway());
        assertEquals(error(520,m), "T5", r.get(1).getHome());
        assertEquals(error(521,m), "T1", r.get(1).getAway());
        r = fs.get(4).getMatches();
        assertEquals(error(522,m), 2,    r.size());
        assertEquals(error(523,m), "T3", r.get(0).getHome());
        assertEquals(error(524,m), "T1", r.get(0).getAway());
        assertEquals(error(525,m), "T4", r.get(1).getHome());
        assertEquals(error(526,m), "T5", r.get(1).getAway()); 
        ts = ls[5].getTeams();
        assertEquals(error(527,m), 5,    ts.size());
        for (int k = 0; k < 5; k++)
            assertEquals(error(528,m), "T" + (k+1), ts.get(k));
        
        ls[7].makeSchedule();
        fs = ls[7].getFixtures();
        assertEquals(error(701,m), 7,    fs.size());
        r = fs.get(0).getMatches();
        assertEquals(error(702,m), 3,    r.size());
        assertEquals(error(703,m), "T2", r.get(0).getHome());
        assertEquals(error(704,m), "T7", r.get(0).getAway());
        assertEquals(error(712,m), "T3", r.get(1).getHome());
        assertEquals(error(713,m), "T6", r.get(1).getAway());
        assertEquals(error(714,m), "T4", r.get(2).getHome());
        assertEquals(error(715,m), "T5", r.get(2).getAway());
        r = fs.get(1).getMatches();
        assertEquals(error(705,m), 3,    r.size());
        assertEquals(error(706,m), "T1", r.get(0).getHome());
        assertEquals(error(707,m), "T6", r.get(0).getAway());
        assertEquals(error(722,m), "T2", r.get(1).getHome());
        assertEquals(error(723,m), "T5", r.get(1).getAway());
        assertEquals(error(724,m), "T3", r.get(2).getHome());
        assertEquals(error(725,m), "T4", r.get(2).getAway());
        r = fs.get(2).getMatches();
        assertEquals(error(708,m), 3,    r.size());
        assertEquals(error(709,m), "T7", r.get(0).getHome());
        assertEquals(error(710,m), "T5", r.get(0).getAway());
        assertEquals(error(732,m), "T1", r.get(1).getHome());
        assertEquals(error(733,m), "T4", r.get(1).getAway());
        assertEquals(error(734,m), "T2", r.get(2).getHome());
        assertEquals(error(735,m), "T3", r.get(2).getAway());
        r = fs.get(3).getMatches();
        assertEquals(error(740,m), 3,    r.size());
        assertEquals(error(741,m), "T6", r.get(0).getHome());
        assertEquals(error(742,m), "T4", r.get(0).getAway());
        assertEquals(error(743,m), "T7", r.get(1).getHome());
        assertEquals(error(744,m), "T3", r.get(1).getAway());
        assertEquals(error(745,m), "T1", r.get(2).getHome());
        assertEquals(error(746,m), "T2", r.get(2).getAway());
        r = fs.get(4).getMatches();
        assertEquals(error(750,m), 3,    r.size());
        assertEquals(error(751,m), "T5", r.get(0).getHome());
        assertEquals(error(752,m), "T3", r.get(0).getAway());
        assertEquals(error(753,m), "T6", r.get(1).getHome());
        assertEquals(error(754,m), "T2", r.get(1).getAway());
        assertEquals(error(755,m), "T7", r.get(2).getHome());
        assertEquals(error(756,m), "T1", r.get(2).getAway());
        r = fs.get(5).getMatches();
        assertEquals(error(760,m), 3,    r.size());
        assertEquals(error(761,m), "T4", r.get(0).getHome());
        assertEquals(error(762,m), "T2", r.get(0).getAway());
        assertEquals(error(763,m), "T5", r.get(1).getHome());
        assertEquals(error(764,m), "T1", r.get(1).getAway());
        assertEquals(error(765,m), "T6", r.get(2).getHome());
        assertEquals(error(766,m), "T7", r.get(2).getAway());
        r = fs.get(6).getMatches();
        assertEquals(error(770,m), 3,    r.size());
        assertEquals(error(771,m), "T3", r.get(0).getHome());
        assertEquals(error(772,m), "T1", r.get(0).getAway());
        assertEquals(error(773,m), "T4", r.get(1).getHome());
        assertEquals(error(774,m), "T7", r.get(1).getAway());
        assertEquals(error(775,m), "T5", r.get(2).getHome());
        assertEquals(error(776,m), "T6", r.get(2).getAway());
        ts = ls[7].getTeams();
        assertEquals(error(711,m), 7,    ts.size());
        for (int k = 0; k < 7; k++)
            assertEquals(error(799,m), "T" + (k+1), ts.get(k));
    }
    
    @Test
    public void testLeaguegetDisplayValue() 
    {
        String m = "League getDisplayValue";
        // using trim allows any whitespace at the ends 
        String[] ss = {"Round 1\ntH0 vs. tA0\ntH1 vs. tA1\ntH2 vs. tA2\n\n",
                       "Round 2\ntH1 vs. tA1\ntH2 vs. tA2\ntH3 vs. tA3\n\n",
                       "Round 3\ntH2 vs. tA2\ntH3 vs. tA3\ntH0 vs. tA0\n\n",
                       "Round 4\ntH3 vs. tA3\ntH0 vs. tA0\ntH1 vs. tA1\n\n",
                       "Round 5\ntH0 vs. tA0\ntH1 vs. tA1\ntH2 vs. tA2\n\n",
                       "Round 6\ntH1 vs. tA1\ntH2 vs. tA2\ntH3 vs. tA3\n\n",
                       "Round 7\ntH2 vs. tA2\ntH3 vs. tA3\ntH0 vs. tA0\n\n",
                       "Round 8\ntH3 vs. tA3\ntH0 vs. tA0\ntH1 vs. tA1\n\n"};
        String soln = "";
        for (int k = 0; k < ss.length; k++)
        {
            ls[4].addRound(rs[k]);
            for (int j = 0; j < 3; j++)
                ls[4].getFixtures().get(k).addMatch(ms[(k+j) % 4]);
            soln += ss[k];
            assertTrue(error(k+1,m), soln.trim().equals(ls[4].getDisplayValue().trim()));
        }
        ls[5].addRound(rs[8]);
        ls[5].getFixtures().get(0).addMatch(ms[0]);
        assertTrue(error(10,m), ls[5].getDisplayValue().trim().equals("Round 1\ntH0 vs. tA0"));
        ls[5].addRound(rs[9]);
        ls[5].getFixtures().get(1).addMatch(ms[1]);
        assertTrue(error(11,m), ls[5].getDisplayValue().trim().equals("Round 1\ntH0 vs. tA0\n\nRound 2\ntH1 vs. tA1"));
    }

    @Test
    public void testLeagueconstructor2() 
    {
        String m = "constructor2";
        String[] pl = {"Earth", "Jupiter", "Mercury", "Mars", "Neptune", "Saturn", "Uranus", "Venus"};
        ArrayList<String> ts = planets.getTeams();
        assertTrue  (error(1,m),    ts != null);
        assertEquals(error(2,m), 8, ts.size());
        for (int i = 0; i < pl.length; i++) 
            assertEquals(error(3,m), pl[i], ts.get(i));
        assertTrue  (error(4,m),    planets.getFixtures() != null);
        assertEquals(error(5,m), 0, planets.getFixtures().size());
    }
}
