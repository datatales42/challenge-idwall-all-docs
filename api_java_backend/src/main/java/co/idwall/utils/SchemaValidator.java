package co.idwall.utils;

import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import co.idwall.exceptions.BadQueryParametersError;
import co.idwall.exceptions.ExactMatchPassedWithFullNameError;
import co.idwall.exceptions.InvalidBirthDateFormatError;
import co.idwall.model.GetWantedsParameters;
import co.idwall.regexs.Regexs;

public class SchemaValidator {
	public void validateExactMatch(Map<String, String> body) {
		if (
				(body.get("exact_match") != null && body.get("alias") == null)
		) {
			throw new ExactMatchPassedWithFullNameError();
		}
	}

//	public void validateBirthDate(Map<String, String> body) {
//		String birthDate = body.get("birth_date");
//
//		if (birthDate == null) return;
//
//        Pattern regex = Regexs.MONTH_DAY_YEAR_DATE.getPattern();
//
//        Matcher regexMatcher = regex.matcher(birthDate);
//
//        if (!regexMatcher.find()) {
//            throw new InvalidBirthDateFormatError();
//        }
//	}

	public GetWantedsParameters validateOtherParameters(Map<String, String> body) {
		GetWantedsParameters parameters = new GetWantedsParameters();

		List<String> allowedQueryParams = ClassUtils.getClassPropertyNames(parameters);

		body.forEach((key, value) -> {
			boolean paramIsValid = allowedQueryParams.contains(key);

			if(!paramIsValid) throw new BadQueryParametersError();

			if(paramIsValid) {
				if (key.equals("wanted_origin_id")) parameters.setWantedOriginId(value);
				if (key.equals("alias")) parameters.setAlias(value);
				if (key.equals("exact_match")) parameters.setExactMatch(Boolean.parseBoolean(value));
				if (key.equals("birth_date")) parameters.setBirthDate(value);
				if (key.equals("distinguishing_marks")) parameters.setDistinguishingMarks(value);
				if (key.equals("nationality")) parameters.setNationality(value);
				if (key.equals("languages")) parameters.setLanguages(value);
				if (key.equals("sex")) parameters.setSex(value);
				if (key.equals("wanted_in")) parameters.setWantedIn(value);
				if (key.equals("charges")) parameters.setCharges(value);
			};
		});

		return parameters;
	}

	public GetWantedsParameters validate(Map<String, String> body) {
		validateExactMatch(body);
//		validateBirthDate(body);

		GetWantedsParameters parameters = validateOtherParameters(body);

		return parameters;
	}
}
