package co.idwall.repository;

import java.util.List;

import org.springframework.data.jpa.domain.Specification;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.stereotype.Repository;

import co.idwall.model.Wanted;

@Repository()
public interface WantedRepository extends JpaRepository<Wanted, String>, JpaSpecificationExecutor<Wanted> {
	List<Wanted> findAll(Specification<Wanted> spec);
}