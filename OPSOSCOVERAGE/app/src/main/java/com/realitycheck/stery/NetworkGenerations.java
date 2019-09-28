package com.realitycheck.stery;

public enum NetworkGenerations {
    none("Неизвестная сеть"),
    net2g("2G"),
    net3g("3G"),
    net4g("4G"),
    net5g("5G");

    private String type;

    NetworkGenerations(String type) {
        this.type = type;
    }

    public String getType() {
        return this.type;
    }
}
