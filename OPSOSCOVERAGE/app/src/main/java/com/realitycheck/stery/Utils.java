package com.realitycheck.stery;

import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.location.Address;
import android.location.Location;
import android.preference.PreferenceManager;
import android.telephony.TelephonyManager;

import com.google.android.gms.location.LocationResult;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

import static android.content.Context.NOTIFICATION_SERVICE;
import static android.content.Context.TELEPHONY_SERVICE;


/**
 * Created by FreakyJolly on 01-04-2018.
 */

public class Utils {
    private static final String TAG = "UtilsClass";
    final static String KEY_LOCATION_UPDATES_RESULT = "location-update-result";
    public static float accuracy;
    static String addressFragments = "";
    static List<Address> addresses = null;
    public static final long UPDATE_INTERVAL = 3 * 1000;
    public static final float SMALLEST_DISPLACEMENT = 1.0F;
    public static final long FASTEST_UPDATE_INTERVAL = UPDATE_INTERVAL / 4;
    public static final long MAX_WAIT_TIME = UPDATE_INTERVAL * 2;

    public static MobileManager mobileManager = null;

    static void setLocationUpdatesResult(Context context, String value) {
        PreferenceManager.getDefaultSharedPreferences(context)
                .edit()
                .putString(KEY_LOCATION_UPDATES_RESULT, value)
                .apply();
    }

//    @SuppressLint("MissingPermission")
    public static void getLocationUpdates(final Context context, final Intent intent, String broadcastevent)  {

        LocationResult result = LocationResult.extractResult(intent);
        if (result != null) {

            Date today = Calendar.getInstance().getTime();
            SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd HH.mm.ss");
            String nowDate = formatter.format(today);


            List<Location> locations = result.getLocations();
            Location firstLocation = locations.get(0);

            //firstLocation.getAccuracy();
            //firstLocation.getLatitude();
            //firstLocation.getLongitude();
            //firstLocation.getAccuracy();
            //firstLocation.getSpeed();
            //firstLocation.getBearing();
            LocationRequestHelper.getInstance(context).setValue("locationTextInApp","You are at "+"("+nowDate+") "+" Latitude:"+firstLocation.getLatitude()+" Longitude:"+firstLocation.getLongitude());

            if (mobileManager == null)
                mobileManager = new MobileManager((TelephonyManager) context.getSystemService(TELEPHONY_SERVICE));

            CollectedData collectedData = new CollectedData();

            collectedData.setOperator(mobileManager.getOperatorName());

            PowerOfTower powerOfTower = mobileManager.getStrengthOfCurrentNetwork();
            collectedData.setSignalStrength(powerOfTower.strength);
            collectedData.setConnectionType(powerOfTower.networkGeneration.getType());

            collectedData.setLatitude(firstLocation.getLatitude());
            collectedData.setLongtitude(firstLocation.getLongitude());

            collectedData.setChecksum(29092019);

            DataTransporter.transfer(collectedData);
            showNotificationOngoing(context, broadcastevent,"");
        }

        //TODO: notify to make commit
    }

    public static void showNotificationOngoing(Context context, String broadcastevent,String title) {
            NotificationManager notificationManager =
                    (NotificationManager) context.getSystemService(NOTIFICATION_SERVICE);

            PendingIntent contentIntent = PendingIntent.getActivity(context, 0,
                    new Intent(context, MainActivity.class), PendingIntent.FLAG_UPDATE_CURRENT);

            Notification.Builder notificationBuilder = new Notification.Builder(context)
                    .setContentTitle(title + DateFormat.getDateTimeInstance().format(new Date()) + ":" + accuracy)
                    .setContentText(addressFragments.toString())
                    .setSmallIcon(R.mipmap.ic_launcher)
                    .setContentIntent(contentIntent)
                    .setOngoing(true)
                    .setStyle(new Notification.BigTextStyle().bigText(addressFragments.toString()))
                    .setAutoCancel(true);
            notificationManager.notify(3, notificationBuilder.build());

    }

    public static void removeNotification(Context context){
        NotificationManager notificationManager =
                (NotificationManager) context.getSystemService(NOTIFICATION_SERVICE);
        notificationManager.cancelAll();
    }
}

