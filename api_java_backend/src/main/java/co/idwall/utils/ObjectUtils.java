package co.idwall.utils;

import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.List;

public class ObjectUtils {
	public static List<String> getKeys(Object obj) {
		List<String> keys = new ArrayList<>();

        Field[] fields = obj.getClass().getDeclaredFields();
        
        for (Field field : fields) {
            field.setAccessible(true);
            
            try {
                Object value = field.get(obj);
                
                if (value != null) {
                    keys.add(field.getName());
                }
            } catch (IllegalAccessException e) {
                e.printStackTrace();
            }
        }

        return keys;
    }
}
