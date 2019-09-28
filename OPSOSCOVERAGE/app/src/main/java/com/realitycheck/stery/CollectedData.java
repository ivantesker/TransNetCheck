package com.realitycheck.stery;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class CollectedData {

    @SerializedName("latitude")
    @Expose
    private double latitude;

    @SerializedName("longtitude")
    @Expose
    private double longtitude;

    @SerializedName("level")
    @Expose
    private int signalStrength;

    @SerializedName("checksum")
    @Expose
    private int checksum;

    @SerializedName("operator")
    @Expose
    private String operator;

    @SerializedName("type")
    @Expose
    private String connectionType;

//    @SerializedName("cellId")
//    @Expose
//    private int cellId;
//
//    @SerializedName("cellLocationCoda")
//    @Expose
//    private int cellLocationCode;

    public double getLatitude() {
        return latitude;
    }

    public void setLatitude(double latitude) {
        this.latitude = latitude;
    }

    public double getLongtitude() {
        return longtitude;
    }

    public void setLongtitude(double longtitude) {
        this.longtitude = longtitude;
    }

    public int getSignalStrength() {
        return signalStrength;
    }

    public void setSignalStrength(int signalStrength) {
        this.signalStrength = signalStrength;
    }

    public int getChecksum() {
        return checksum;
    }

    public void setChecksum(int checksum) {
        this.checksum = checksum;
    }

    public String getOperator() {
        return operator;
    }

    public void setOperator(String operator) {
        this.operator = operator;
    }

    public String getConnectionType() {
        return connectionType;
    }

    public void setConnectionType(String connectionType) {
        this.connectionType = connectionType;
    }

//    public int getCellId() {
//        return cellId;
//    }
//
//    public void setCellId(int cellId) {
//        this.cellId = cellId;
//    }
//
//    public int getCellLocationCode() {
//        return cellLocationCode;
//    }
//
//    public void setCellLocationCode(int cellLocationCode) {
//        this.cellLocationCode = cellLocationCode;
//    }



}
