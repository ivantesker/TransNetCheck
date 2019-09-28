package com.realitycheck.stery;

import android.annotation.SuppressLint;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.TaskStackBuilder;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.provider.Settings;
import android.support.v4.app.NotificationCompat;
import android.support.v4.content.ContextCompat;
import android.telephony.CellInfo;
import android.telephony.CellInfoCdma;
import android.telephony.CellInfoGsm;
import android.telephony.CellInfoLte;
import android.telephony.CellInfoWcdma;
import android.telephony.TelephonyManager;
import android.telephony.gsm.GsmCellLocation;
import android.util.Log;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class MobileManager {

    private TelephonyManager telephonyManager;

    public MobileManager(TelephonyManager telephonyManager){
        this.telephonyManager = telephonyManager;
    }

    public void getCellTowerLoc(){
        @SuppressLint("MissingPermission")
        GsmCellLocation cellLocation = (GsmCellLocation)telephonyManager.getCellLocation();
        int cellid= cellLocation.getCid();
        int celllac = cellLocation.getLac();

        Log.d("CellLocation", cellLocation.toString());
        Log.d("GSM CELL ID",  Integer.valueOf(cellid).toString());
        Log.d("GSM Location Code", Integer.valueOf(celllac).toString());
    }

    public String getOperatorName(){
        return telephonyManager.getNetworkOperatorName();
    }

    public PowerOfTower getStrengthOfCurrentNetwork(){
        @SuppressLint("MissingPermission")
        List<CellInfo> cellInfoList = telephonyManager.getAllCellInfo();
        NetworkGenerations bestType = NetworkGenerations.none;
        int strength = 99;

        for (CellInfo cellInfo : cellInfoList)
        {
            if (cellInfo instanceof CellInfoGsm) {
                strength = ((CellInfoGsm)cellInfo).getCellSignalStrength().getDbm();
                bestType = NetworkGenerations.net2g;
            }
            else if (cellInfo instanceof CellInfoCdma){
                int temp = ((CellInfoCdma)cellInfo).getCellSignalStrength().getDbm();
                if (temp < strength){
                    bestType = NetworkGenerations.net3g;
                    strength = temp;
                }
            }
            else if (cellInfo instanceof CellInfoWcdma){
                int temp = ((CellInfoWcdma)cellInfo).getCellSignalStrength().getDbm();
                if (temp < strength){
                    bestType = NetworkGenerations.net3g;
                    strength = temp;
                }
            }
            else if (cellInfo instanceof CellInfoLte){
                strength = ((CellInfoLte)cellInfo).getCellSignalStrength().getDbm();
                bestType = NetworkGenerations.net4g;
            }
        }
        return new PowerOfTower(bestType, strength);
    }

    public static boolean isAirplaneModeOn(Context context) {
        return Settings.System.getInt(context.getContentResolver(),
                Settings.Global.AIRPLANE_MODE_ON, 0) != 0;

    }

    public static void notification(String title, String message, Context context) {
        NotificationManager notificationManager = (NotificationManager) context.getSystemService(Context.NOTIFICATION_SERVICE);

        int notificationId = createID();
        String channelId = "channel-id";
        String channelName = "Channel Name";
        int importance = NotificationManager.IMPORTANCE_DEFAULT;

        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            NotificationChannel mChannel = new NotificationChannel(
                    channelId, channelName, importance);
            notificationManager.createNotificationChannel(mChannel);
        }

        NotificationCompat.Builder mBuilder = new NotificationCompat.Builder(context, channelId)
                .setSmallIcon(R.drawable.ic_launcher_foreground)//R.mipmap.ic_launcher
                .setContentTitle(title)
                .setContentText(message)
                .setVibrate(new long[]{100, 250})
                .setLights(Color.YELLOW, 500, 5000)
                .setAutoCancel(true)
                .setColor(ContextCompat.getColor(context, R.color.colorPrimary));

        TaskStackBuilder stackBuilder = TaskStackBuilder.create(context);
        stackBuilder.addNextIntent(new Intent(context, MainActivity.class));
        PendingIntent resultPendingIntent = stackBuilder.getPendingIntent(0, PendingIntent.FLAG_UPDATE_CURRENT);
        mBuilder.setContentIntent(resultPendingIntent);

        notificationManager.notify(notificationId, mBuilder.build());

    }

    public static int createID() {
        Date now = new Date();
        return Integer.parseInt(new SimpleDateFormat("ddHHmmss", Locale.getDefault()).format(now));
    }
}
