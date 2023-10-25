package co.idwall.utils;

import java.util.ArrayList;
import java.util.List;
import java.lang.reflect.Field;

public class ClassUtils {
    public static List<String> getClassPropertyNames(Object obj) {
        Class<?> clazz = obj.getClass();
        
        Field[] fields = clazz.getDeclaredFields();
        
        List<String> keys = new ArrayList<>();

        for (Field field : fields) {
            keys.add(field.getName());
        }

        return keys;
    }
}
