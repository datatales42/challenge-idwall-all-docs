package co.idwall.resources;

import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import co.idwall.business.GetWantedBusiness;
import co.idwall.errors.ErrorResponses;
import co.idwall.exceptions.BadQueryParametersError;
import co.idwall.exceptions.ExactMatchPassedWithFullNameError;
import co.idwall.exceptions.InvalidBirthDateFormatError;
import co.idwall.exceptions.WantedNotFound;
import co.idwall.model.GetWantedsParameters;
import co.idwall.responses.ErrorResponse;
import co.idwall.responses.GetWantedsResponse;
import co.idwall.utils.SchemaValidator;

@RestController
@RequestMapping("wanteds")
public class WantedController {
	private GetWantedBusiness business;
	
	@Autowired
    public WantedController(GetWantedBusiness business) {
		this.business = business;
    }
	
	@GetMapping()
    public ResponseEntity<?> getWanteds(@RequestParam Map<String, String> queryParameters) {
		try {
			SchemaValidator validator = new SchemaValidator();
			
			GetWantedsParameters parameters = validator.validate(queryParameters);
			
			business.setParameters(parameters);
			
			GetWantedsResponse response = business.getWanteds();

			return ResponseEntity.status(HttpStatus.OK).body(response);
		} catch (BadQueryParametersError e) {
			ErrorResponse response = ErrorResponses.getBadQueryParametersResponse();

			return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(response);
		} catch (WantedNotFound e) {
			ErrorResponse response = ErrorResponses.getNotFoundWantedResponse();

			return ResponseEntity.status(HttpStatus.NOT_FOUND).body(response);
		} catch (ExactMatchPassedWithFullNameError e) {
			ErrorResponse response = ErrorResponses.getExactMatchPassedWithFullNameResponse();

			return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(response);
		} catch (InvalidBirthDateFormatError e) {
			ErrorResponse response = ErrorResponses.getInvalidBirthDateFormatResponse();

			return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(response);
		}  catch (Exception e) {
			ErrorResponse response = ErrorResponses.getProblemsCallingAPIResponse();
			System.out.println(e);
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
		}
    }
}
