package co.idwall.responses;

import java.util.List;

import co.idwall.model.Wanted;

public class GetWantedsResponse {
	private List<Wanted> potential_matches;

	public GetWantedsResponse(List<Wanted> potential_matches) {
		super();
		this.potential_matches = potential_matches;
	}

	public List<Wanted> getPotential_matches() {
		return potential_matches;
	}

	public void setPotential_matches(List<Wanted> potential_matches) {
		this.potential_matches = potential_matches;
	}
}
