/**
 * Models a round of matches in a league schedule.
 * 
 * @author Thomas Cleary (21704985)
 * @version v1.02
 */
import java.util.ArrayList;

public class Round
{
    // the list of matches
    private ArrayList<Match> matches;

    /**
     * Creates an empty round of matches.
     */
    public Round()
    {
        matches = new ArrayList<>();
    }
    
    /**
     * Returns the list of matches.
     */
    public ArrayList<Match> getMatches()
    {
        return matches;
    }
    
    /**
     * Adds the provided match at the end of the round.
     */
    public void addMatch(Match match)
    {
        matches.add(match);
    }
    
    /**
     * Removes the indicated match from the round, if the index is legal.
     */
    public void deleteMatch(int index)
    {
        if(index >= 0 && index < matches.size()) {
            matches.remove(index);
        }
    }
    
    /**
     * Makes a round of matches for the provided teams. 
     * Teams 0 & 1 play each other (Team 0 at home iff the second argument is true), then 
     * Team 2 is at home to the last team, Team 3 is at home to the next-to-last team, and so on. 
     * e.g. for six teams A,B,C,D,E,F and second argument true, 
     * we would get the three matches A vs. B, C vs. F, D vs. E. 
     * e.g. for eight teams A,B,C,D,E,F,G,H and second argument false, 
     * we would get the four matches B vs. A, C vs. H, D vs. G, E vs. F. 
     * You may assume that teams.size() >= 2 and teams.size() is even. 
     */
    public void makeRound(ArrayList<String> teams, boolean b)
    {   
        // empties the matches ArrayList so that multiple calls to makeRound() 
        // don't accumulate within the same ArrayList
        matches.clear();
        
        if(b) {
            addMatch(new Match(teams.get(0), teams.get(1))); // add match1: t1h vs t2a
        }
        else {
            addMatch(new Match(teams.get(1), teams.get(0))); // add match1: t2h vs t1a
        }
        
        int numTeams = teams.size();
        int home = 2;
        int away = numTeams - 1;
        
        // create remaining matches for the round and add them to matches
        for(int x = 0; x < numTeams/2 - 1; x++) {
            addMatch(new Match(teams.get(home), teams.get(away)));
            home += 1;
            away -= 1;
        }
    }
    
    /**
     * Returns a string describing this round of matches. 
     * See the project description for the required format. 
     */
    public String getDisplayValue()
    {
        String round_matches = "";
        
        for(Match match : matches) {
            round_matches += match.getDisplayValue() + "\n";
        }
        return round_matches;
    }
}
