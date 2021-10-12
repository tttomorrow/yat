import java.io.*;
import java.sql.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Properties;

/**
 **/
public class jdbc_set_readonly {
    static public String driver = "org.postgresql.Driver";
    public static Properties getConfigFromFile(String filePath) {
        Properties props = new Properties();
        try {
            BufferedInputStream config = new BufferedInputStream(new FileInputStream(filePath));
            props.load(config);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return props;
    }

    public static String genURLFromPro(Properties props) {
        String hostname = props.getProperty("hostname");
        String[] hostnames = hostname.split(",");
        String port = props.getProperty("port");
        String[] ports = port.split(",");
        String dbname = props.getProperty("dbname");
        return genURLFromHostsPortsDBname(hostnames, ports, dbname);
    }

    public static String genURLFromHostsPortsDBname(String[] hostnames, String[] ports, String dbname) {
        String sourceURL;
        if (hostnames.length == 1) {
            sourceURL = "jdbc:postgresql://" + hostnames[0] + ":" + ports[0] + "/" + dbname;
        } else {
            ArrayList<String> ip_port_pare = new ArrayList<>();
            if (ports.length == 1) {
                for (String ip : hostnames) {
                    ip_port_pare.add(ip + ":" + ports[0]);
                }
            } else {
                for (int i = 0; i < hostnames.length; i++) {
                    ip_port_pare.add(hostnames[i] + ":" + ports[i]);
                }
            }
            sourceURL = "jdbc:postgresql://" + String.join(",", ip_port_pare) + "/" + dbname;
        }
        return sourceURL;
    }

    public static Connection GetConnection(Properties props, String user, String passwd) {
        Connection connR;
        String sourceURL = genURLFromPro(props);
        props.put("user", user);
        props.put("password", passwd);
        try {
            Class.forName(driver).newInstance();
            connR = DriverManager.getConnection(sourceURL, props);
        } catch (Exception var10) {
            var10.printStackTrace();
            return null;
        }
        return connR;
    }

    public static Connection GetConnection(Properties props) {
        Connection connR;
        String sourceURL = genURLFromPro(props);
        try {
            Class.forName(driver).newInstance();
            connR = DriverManager.getConnection(sourceURL, props);
        } catch (Exception var10) {
            var10.printStackTrace();
            return null;
        }
        return connR;
    }

    public static void main(String[] args) {
        Properties pros = new Properties();
        Properties pros_conf=null;
        String jdbc_config_file = null;
        for (int i = 0; i < args.length; i++) {
            switch (args[i]) {
                case "--config-file":
                    jdbc_config_file = args[i + 1];
                    pros_conf=getConfigFromFile(jdbc_config_file);
                    break;
                case "-F":
                    jdbc_config_file = args[i + 1];
                    pros_conf=getConfigFromFile(jdbc_config_file);
                    break;
                case "-u":
                    pros.put("user", args[i + 1]);
                    break;
                case "--user-name":
                    pros.put("user", args[i + 1]);
                    break;
                case "-W":
                    pros.put("password", args[i + 1]);
                    break;
                case "--password":
                    pros.put("password", args[i + 1]);
                    break;
                case "-d":
                    pros.put("dbname", args[i + 1]);
                    break;
                default:
                    break;
            }
        }
        //建立连接
        if (pros_conf!=null){
            //以参数为准，覆盖配置文件中的
            pros_conf.putAll(pros);
            System.out.println(pros_conf);
        }
        Connection conn = GetConnection(pros_conf);
        System.out.println(conn);
        if(conn==null){
            System.out.println("连接失败");
            return;
        }else{
            try{
                System.out.println("1.expect result is false, actual result is : " + conn.isReadOnly());
                conn.setReadOnly(true);
                String sql = "show default_transaction_read_only";
                PreparedStatement ps_insert=conn.prepareStatement(sql);
                ResultSet rs=ps_insert.executeQuery();
                while(rs.next()){
                    String result = rs.getString(1);
                    System.out.println("2.expect result is on, actual result is :" + result);
                }
                System.out.println("3.expect result is true, actual result is : " + conn.isReadOnly());
                conn.setReadOnly(false);
                ps_insert=conn.prepareStatement(sql);
                rs=ps_insert.executeQuery();
                while(rs.next()){
                    String result = rs.getString(1);
                    System.out.println("4.expect result is off, actual result is :" + result);
                }
                System.out.println("5.expect result is false, actual result is : " + conn.isReadOnly());
            }catch (SQLException s){
                s.printStackTrace();
            }
        }
        try{
            conn.close();
        }catch (SQLException s){
            s.printStackTrace();
        }
        
    }
}