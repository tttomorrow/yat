"""
Copyright (c) 2022 Huawei Technologies Co.,Ltd.

openGauss is licensed under Mulan PSL v2.
You can use this software according to the terms and conditions of the Mulan PSL v2.
You may obtain a copy of Mulan PSL v2 at:

          http://license.coscl.org.cn/MulanPSL2

THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
See the Mulan PSL v2 for more details.
"""
import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.sql.*;
import java.util.ArrayList;
import java.util.Properties;


/**
 **/
public class jdbc_preparethreshold_case0001 {
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
        String sourceURL1 = sourceURL + "?prepareThreshold=1&currentSchema=public&autosave=always";
        return sourceURL1;
    }

    public static Connection GetConnection(Properties props) {
        Connection connR;
        String sourceURL = genURLFromPro(props);
        System.out.println(sourceURL);
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
                default:
                    break;
            }
        }
        //建立连接
        if (pros_conf!=null){
            //以参数为准，覆盖配置文件中的
            pros_conf.putAll(pros);
        }
        Connection conn = GetConnection(pros_conf);
        System.out.println(conn);
        if(conn==null){
            System.out.println("连接失败");
            return;
        }else{
            Statement stmt = null;
            PreparedStatement pstmt = null;
            PreparedStatement pstmt2 = null;
            try{
                stmt = conn.createStatement();
                conn.setAutoCommit(false);
                int rc = stmt.executeUpdate("set enable_bitmapscan =off;"); // P B E
                rc = stmt.executeUpdate("set enable_seqscan =off;"); // P B E
                //int rc = stmt.executeUpdate("set enable_light_proxy =off;"); // P B E
                stmt.close();
                String selectSql = "select c2 from test where id =? ;";//order by id;";
                String selectSql2 = "select name from test where id =? ;";
                // stmt = conn.createStatement();
                pstmt = conn.prepareStatement(selectSql);
                pstmt2 = conn.prepareStatement(selectSql2);
                pstmt.setFetchSize(1);
                pstmt2.setFetchSize(3);
                pstmt.setInt(1,1);
                pstmt2.setInt(1,2);
                ResultSet rs = pstmt.executeQuery(); // P1 B1 E1
                int round =0;
                while(rs.next()){ //E1 E1 E1
                    System.err.println("c2="+rs.getInt(1));
                    System.err.println();
                    round++;
                    if(round == 4)
                        break;
                }
                //conn.rollback();
                rs = pstmt.executeQuery();
                System.err.println("break of a resultset of pstmt1");
                round = 0;
                rs = pstmt.executeQuery();
                stmt = conn.createStatement();
                int rc2 = stmt.executeUpdate("update test set name = 'xx' where c2 = 1;"); // P B E
                // conn.rollback();
                stmt.close();
                //pstmt.setInt(1,2);
                ResultSet rs2 = pstmt2.executeQuery(); // P2 B2 E2
                while(rs2.next()){ // E2
                    System.err.println("name="+rs2.getString(1));
                    System.err.println();
                    round++;
                    if (round == 6)
                        break;
                }
                System.err.println("break of a resultset of pstmt2");
                round = 0;
                while(rs.next()) { //
                    System.err.println("c2="+rs.getInt(1));
                    System.err.println();
                    round++;
                    if (round == 6)
                        break;
                }
                System.err.println("end of a resultset");
                pstmt.close();
                pstmt2.close();
            }catch (SQLException e){
                if (pstmt != null) {
                    try {
                        pstmt.close();
                    } catch (SQLException e1) {
                        e1.printStackTrace();
                    }
                }
                if (stmt != null) {
                    try {
                        stmt.close();
                    } catch (SQLException e1) {
                        e1.printStackTrace();
                    }
                }
                e.printStackTrace();
                    }
        try{
            conn.close();
        }catch (SQLException s){
            s.printStackTrace();
        }
        }

    }
}