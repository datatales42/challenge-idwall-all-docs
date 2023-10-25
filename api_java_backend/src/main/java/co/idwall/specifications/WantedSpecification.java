package co.idwall.specifications;

import org.springframework.data.jpa.domain.Specification;
import javax.persistence.criteria.Predicate;
import javax.persistence.criteria.Root;
import javax.persistence.criteria.CriteriaQuery;
import javax.persistence.criteria.CriteriaBuilder;

import co.idwall.model.WantedSearchCriteria;
import co.idwall.model.Wanted;

public class WantedSpecification implements Specification<Wanted> {
    private WantedSearchCriteria criteria;

    public WantedSpecification(WantedSearchCriteria criteria) {
        this.criteria = criteria;
    }

    @Override
    public Predicate toPredicate(Root<Wanted> root, CriteriaQuery<?> query, CriteriaBuilder builder) {
        Predicate predicate = builder.conjunction();

        if (criteria.getAliases() != null) {
            predicate = builder.and(predicate, builder.equal(root.get("aliases"), criteria.getAliases()));
        }

        return predicate;
    }
}
