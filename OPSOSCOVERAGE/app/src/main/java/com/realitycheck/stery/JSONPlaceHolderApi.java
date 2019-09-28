package com.realitycheck.stery;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.POST;
import retrofit2.http.Query;

public interface JSONPlaceHolderApi {
    @POST("/signals")
    public Call<CollectedData> sendPacked(@Body CollectedData data);

    @POST("/signals")
    public Call<CollectedData> sendFields(@Query("latitude") double lat,
                                           @Query("longtitude") double lon,
                                           @Query("level") int level,
                                           @Query("checksum") int checksum,
                                           @Query("operator") String operator,
                                           @Query("type") String type
                                           );

}