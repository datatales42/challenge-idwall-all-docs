package co.idwall.business;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.stereotype.Service;

import co.idwall.exceptions.WantedNotFound;
import co.idwall.model.GetWantedsParameters;
import co.idwall.model.Wanted;
import co.idwall.model.WantedSearchCriteria;
import co.idwall.repository.WantedRepository;
import co.idwall.responses.GetWantedsResponse;
import co.idwall.specifications.WantedSpecification;
import co.idwall.utils.ObjectUtils;

import javax.persistence.criteria.Predicate;

@Service
public class GetWantedBusiness {
	@Autowired
    private WantedRepository repository;
    
	private GetWantedsParameters parameters;
	
	public GetWantedBusiness() {}
		
	public GetWantedsResponse getWanteds() {
		List<Wanted> wanteds = getWantedsAccordingToParameters();
		return new GetWantedsResponse(wanteds);
    }
	
	private List<Wanted> getWantedsAccordingToParameters() {		
		boolean hasQueryParameters = !ObjectUtils.getKeys(parameters).isEmpty();
		if(!hasQueryParameters) return repository.findAll();

		String wantedOriginIdParam = parameters.getWantedOriginId();
		String aliasParam = parameters.getAlias();
		boolean exactMatchParam = parameters.getExactMatch();
		String charges = parameters.getCharges();
		String wantedIn = parameters.getWantedIn();
		String birthDate = parameters.getBirthDate();
		String distinguishingMarks = parameters.getDistinguishingMarks();
		String languages = parameters.getLanguages();
		String sex = parameters.getSex();
//
//		if(wantedOriginIdParam != null) {
//			Optional<Wanted> wanted = repository.findById(wantedOriginIdParam);
//			if(wanted.isEmpty()) throw new WantedNotFound();
//			return List.of(wanted.get());
//		}
//
//		if (aliasParam != null) {
//			List<Wanted> wanted;
//			if (exactMatchParam) {
//				wanted = repository.findByAliases(aliasParam);
//			} else {
//				wanted = repository.findByAliasesContaining(aliasParam);
//			}
//			if (wanted.isEmpty())
//				throw new WantedNotFound();
//			return wanted;
//		}
//
//		return null;

		Specification<Wanted> specification = (root, query, criteriaBuilder) -> {
			Predicate combinedCondition = criteriaBuilder.conjunction();
			if(aliasParam != null){
				if (exactMatchParam) {
					Predicate exactMatchCondition = criteriaBuilder.equal(root.get("aliases"), aliasParam);
					combinedCondition = criteriaBuilder.and(combinedCondition, exactMatchCondition);
				} else {
					Predicate partialMatchCondition = criteriaBuilder.like(root.get("aliases"), "%" + aliasParam + "%");
					combinedCondition = criteriaBuilder.and(combinedCondition, partialMatchCondition);
				}
			}
			if(wantedOriginIdParam != null){
				combinedCondition = criteriaBuilder.and(combinedCondition,
						criteriaBuilder.equal(root.get("wanted_origin_id"), wantedOriginIdParam)
				);
			}
			if(charges != null){
				combinedCondition = criteriaBuilder.and(combinedCondition,
						criteriaBuilder.like(root.get("charges"), "%" + charges + "%")
				);
			}
			if(wantedIn != null){
				combinedCondition = criteriaBuilder.and(combinedCondition,
						criteriaBuilder.like(root.get("wanted_in"), "%" + wantedIn + "%")
				);
			}
			if(birthDate != null){
				combinedCondition = criteriaBuilder.and(combinedCondition,
						criteriaBuilder.like(root.get("dates_of_birth_used"), "%" + birthDate + "%")
				);
			}
			if(distinguishingMarks != null){
				combinedCondition = criteriaBuilder.and(combinedCondition,
						criteriaBuilder.like(root.get("distinguishing_marks"), "%" + distinguishingMarks + "%")
				);
			}
			if(languages != null){
				combinedCondition = criteriaBuilder.and(combinedCondition,
						criteriaBuilder.like(root.get("languages"), "%" + languages + "%")
				);
			}
			if(sex != null){
				combinedCondition = criteriaBuilder.and(combinedCondition,
						criteriaBuilder.equal(root.get("sex"), sex)
				);
			}

			return combinedCondition;
		};

		return repository.findAll(specification);
	}

	public void setParameters(GetWantedsParameters parameters) {
		this.parameters = parameters;
	}
}
