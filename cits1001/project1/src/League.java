/**                                                                             
 * Models a league with a set of teams and a schedule of matches between them
 * 
 * @author Thomas Cleary (21704985)
 * @version v1.02
 */
import java.util.ArrayList;

public class League
{
    // the teams in the league
    private ArrayList<String>  teams;
    // the schedule of matches
    private ArrayList<Round> fixtures;

    /**
     * Creates an object with noOfTeams teams named T1, T2, T3, etc. and an empty schedule.
     * You may assume that noOfTeams >= 0. 
     */
    public League(int noOfTeams)
    {
        fixtures = new ArrayList<>();
        teams = new ArrayList<>();
        
        for(int x = 1; x <= noOfTeams; x++) {
            teams.add("T" + x);
        }
    }

    /**
     * Creates an object with the team names from filename (one per line) and an empty schedule. 
     * Uses FileIO to read the file. 
     * You may assume that filename is a valid text file. 
     */
    public League(String filename)
    {
        fixtures = new ArrayList<>();
        teams = new FileIO(filename).getLines();
    }
    
    /**
     * Returns the teams in the league.
     */
    public ArrayList<String> getTeams()
    {
        return teams;
    }
    
    /**
     * Returns the fixtures for the league.
     */
    public ArrayList<Round> getFixtures()
    {
        return fixtures;
    }
    
    /**
     * Adds the provided round to the end of the schedule.
     */
    public void addRound(Round r)
    {
        fixtures.add(r);
    }
    
    /**
     * Moves the last item on teams to index 1 on the list.
     * e.g. <"A", "B", "C", "D"> would become <"A", "D", "B", "C">. 
     * You may assume that teams.size() >= 2. 
     */
    public void rotateTeams()
    {
        teams.add(1, teams.get(teams.size()-1));
        teams.remove(teams.size()-1);
    }
    
    /**
     * Makes a schedule for teams, if there are an even number of them. 
     * Generate teams.size()-1 rounds, rotating the teams between each one. 
     * Team 0 should be at home in the first round, then it should alternate home and away. 
     * See the project description for some examples. 
     * You may assume that teams.size() >= 2 and teams.size() is even. 
     */
    public void makeEvenSchedule()
    {
        // empties fixtures ArrayList so that multiple calls to 
        // makeEvenSchedule don't accumulate within the same ArrayList
        fixtures.clear();
        
        int numRounds = teams.size() - 1;
        boolean t1Home = true;
        
        for(int x = 0; x < numRounds; x++) {
            Round round = new Round();
            round.makeRound(teams, t1Home);
            addRound(round);
            rotateTeams();
            t1Home = !t1Home;
        }
    }
    
    /**
     * Makes a schedule for teams. 
     * If there are an odd number of them, add a dummy team at the front of the list, 
     * then at the end of the process delete the dummy and all of its matches. 
     * See the project description for some examples. 
     * You may assume that teams.size() >= 2. 
     */
    public void makeSchedule()
    {
        if(teams.size() % 2 == 0) { 
            makeEvenSchedule();
        }
        else{
            teams.add(0, "dummy");
            makeEvenSchedule();
            
            for(Round round : fixtures) {
                round.deleteMatch(0);
            }
            teams.remove(0);
        }
    }

    /**
     * Returns a string describing the schedule.
     * See the project description for the required format.
     */
    public String getDisplayValue()
    {
        String schedule = "";
        int roundNum = 1;
        
        for(Round round: fixtures) {
            schedule += "Round " + roundNum + "\n" + round.getDisplayValue() + "\n";
            roundNum += 1;
        }
        
        return schedule;
    }
    
    /**
     * Prints the schedule. 
     */
    public void print()
    {
        System.out.println(getDisplayValue());
    }
}
