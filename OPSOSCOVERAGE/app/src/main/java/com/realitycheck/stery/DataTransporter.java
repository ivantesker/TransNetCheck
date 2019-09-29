package com.realitycheck.stery;

import android.support.annotation.NonNull;
import android.util.Log;

import java.io.IOException;

import okhttp3.RequestBody;
import okio.Buffer;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class DataTransporter {
    private static String bodyToString(final RequestBody request){
        try {
            final RequestBody copy = request;
            final Buffer buffer = new Buffer();
            copy.writeTo(buffer);
            return buffer.readUtf8();
        }
        catch (final IOException e) {
            return "did not work";
        }
    }
    public static boolean transfer(CollectedData data){
        try {
//                CollectedData sc = new CollectedData();
//                sc.setLatitude((float)(Math.random() * 100 % 100 + 0.1));
//                sc.setLongtitude((float)1111.99);
//                sc.setLevel((int)11111);
//                sc.setChecksum((int)111111);
//                sc.setOperator("111111");
//                sc.setType("11111111");
//                Log.i("NETWOW -> ", sc.toString());
//                Call<CollectedData> call = NetworkService.getInstance().getJSONApi().sendPacked(sc);
            Call<CollectedData> call = NetworkService.getInstance().getJSONApi().sendPacked(data);
//            Call<CollectedData> call = NetworkService.getInstance().getJSONApi().sendFields(Math.random() * 100 % 100 + 0.1, 333, 333, 333, "333", "333");
            Log.i("NETWOW -----> ", call.request().url().toString());
            call.enqueue(new Callback<CollectedData>() {
                @Override
                public void onResponse(@NonNull Call<CollectedData> call, @NonNull Response<CollectedData> response) {
                    Log.i("NETWOW msg <- ", response.message());
                    Log.i("NETWOW raw <- ", response.raw().toString());
                    Log.i("NETWOW our body <- ", bodyToString(call.request().body()));
//                                Log.i("NETWOW <- ", );
                }

                @Override
                public void onFailure(@NonNull Call<CollectedData> call, @NonNull Throwable t) {
                    Log.i("NETWOW <- ERR", t.getMessage());
                }
            });
        }
        catch (Exception e) {
            e.printStackTrace();
            return false;
        }
        return true;
    }
}
