package co.idwall.regexs;

import java.util.regex.Pattern;

public enum Regexs {
    MONTH_DAY_YEAR_DATE(compile("\\d{2}-\\d{2}-\\d{4}"));

    private final Pattern pattern;

    Regexs(Pattern pattern) {
        this.pattern = pattern;
    }

    public Pattern getPattern() {
        return pattern;
    }
    
    private static Pattern compile(String stringRegex) {
        return Pattern.compile(stringRegex);
    }
}