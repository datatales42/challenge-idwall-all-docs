package co.idwall.model;

public class GetWantedsParameters {
	private String wanted_origin_id;
	private String alias;
    private boolean exact_match;
    private String birth_date;
    private String distinguishing_marks;
    private String nationality;
    private String languages;
    private String sex;
    private String wanted_in;
    private String charges;
    
	public GetWantedsParameters() {	
		super();
	}
    
	public String getWantedOriginId() {
		return wanted_origin_id;
	}
	
	public void setWantedOriginId(String wanted_origin_id) {
		this.wanted_origin_id = wanted_origin_id;
	}
	
	public String getAlias() {
		return alias;
	}
	
	public void setAlias(String alias) {
		this.alias = alias;
	}
	
	public boolean getExactMatch() {
		return exact_match;
	}
	
	public void setExactMatch(boolean exact_match) {
		this.exact_match = exact_match;
	}
	
	public String getBirthDate() {
		return birth_date;
	}
	
	public void setBirthDate(String birth_date) {
		this.birth_date = birth_date;
	}
	
	public String getDistinguishingMarks() {
		return distinguishing_marks;
	}
	
	public void setDistinguishingMarks(String distinguishing_marks) {
		this.distinguishing_marks = distinguishing_marks;
	}
	
	public String getNationality() {
		return nationality;
	}
	
	public void setNationality(String nationality) {
		this.nationality = nationality;
	}
	
	public String getLanguages() {
		return languages;
	}
	
	public void setLanguages(String languages) {
		this.languages = languages;
	}
	
	public String getSex() {
		return sex;
	}
	
	public void setSex(String sex) {
		this.sex = sex;
	}
	
	public String getWantedIn() {
		return wanted_in;
	}
	
	public void setWantedIn(String wanted_in) {
		this.wanted_in = wanted_in;
	}

	public String getCharges() {
		return charges;
	}
	
	public void setCharges(String charges) {
		this.charges = charges;
	}    
}
