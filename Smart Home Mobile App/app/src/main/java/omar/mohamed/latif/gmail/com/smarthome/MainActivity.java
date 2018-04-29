package omar.mohamed.latif.gmail.com.smarthome;

import android.Manifest;
import android.content.pm.ActivityInfo;
import android.content.pm.PackageManager;
import android.location.Location;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.TextView;

import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationCallback;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationResult;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.location.LocationSettingsRequest;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.List;

public class MainActivity extends AppCompatActivity {

//    private EditText receiveIpEditText;
//    private EditText receivePortEditText;
    private FusedLocationProviderClient mFusedLocationClient;
    private LocationRequest mLocationRequest;
    private LocationCallback mLocationCallback;

    private EditText sendIpEditText;
    private EditText sendPortEditText;

    private TextView runningTextView;

    private TextView ipTextView;

//    private TextView providerTextView;

    private TextView locationTextView;

    private EditText boardNameEditText;

    private CheckBox sendAutoCheckBox;

//    private TextView receivedTextView;

//    private TcpClient mTcpClientReceive;
    private TcpClient mTcpClientSend;



    private double longitude=0;
    private double latitude=0;
    boolean mRequestingLocationUpdates;
    private String REQUESTING_LOCATION_UPDATES_KEY="requestingLocationUpdates";

    private void createLocationRequest() {
        mLocationRequest = new LocationRequest();
        mLocationRequest.setInterval(10000);
        mLocationRequest.setFastestInterval(2000);
        mLocationRequest.setPriority(LocationRequest.PRIORITY_HIGH_ACCURACY);

        LocationSettingsRequest.Builder builder = new LocationSettingsRequest.Builder()
                .addLocationRequest(mLocationRequest);
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (mRequestingLocationUpdates) {
            startLocationUpdates();
        }
    }

    @Override
    protected void onPause() {
        super.onPause();
        stopLocationUpdates();
    }

    @Override
    protected void onSaveInstanceState(Bundle outState) {
        outState.putBoolean(REQUESTING_LOCATION_UPDATES_KEY,
                mRequestingLocationUpdates);
        // ...
        super.onSaveInstanceState(outState);
    }

    private void stopLocationUpdates() {
        mFusedLocationClient.removeLocationUpdates(mLocationCallback);
    }

    private void startLocationUpdates() {

        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.ACCESS_FINE_LOCATION},1);
        }


        mFusedLocationClient.requestLocationUpdates(mLocationRequest,
                mLocationCallback,
                null /* Looper */);
    }

    private void initLocationCallback()
    {
        mLocationCallback = new LocationCallback() {
            @Override
            public void onLocationResult(LocationResult locationResult) {
                if (locationResult == null) {
                    return;
                }
                List<Location> locations=locationResult.getLocations();
                if(locations.size()>0)
                {
                    longitude = locations.get(0).getLongitude();
                    latitude = locations.get(0).getLatitude();
                    locationTextView.setText("(" + String.valueOf(longitude) + "," + String.valueOf(latitude) + ")");
                    if (sendAutoCheckBox.isChecked()) {
                        sendLocation();
                    }
                }

            };
        };

    }

    private void initLocationModule()
    {
        createLocationRequest();
        mFusedLocationClient = LocationServices.getFusedLocationProviderClient(this);
        initLocationCallback();
        startLocationUpdates();

//        LocationManager lm = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
//
//        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
//            ActivityCompat.requestPermissions(this,
//                    new String[]{Manifest.permission.ACCESS_FINE_LOCATION},1);
//
//        }
//
//        lm.requestLocationUpdates(LocationManager.PASSIVE_PROVIDER, 2000, 2, locationListener);

    }



    private void initConnectingButton()
    {
        Button connectButton=(Button)findViewById(R.id.connect_button);

        connectButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                ipTextView.setText("My Ip: " + Utils.getIPAddress(true));
                runningTextView.setVisibility(View.VISIBLE);
//                new ConnectRecvTask().executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);
                new ConnectSendTask().executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);

            }
        });
    }


    private void initSendManuallyButton()
    {
        Button sendButton=(Button)findViewById(R.id.send_manually_button);

        sendButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                sendLocation();
            }
        });
    }



    private void initUIElements()
    {
//        receiveIpEditText=(EditText)findViewById(R.id.ip_recieve_edit_text);
//        receivePortEditText=(EditText)findViewById(R.id.receive_port_edit_text);

        sendIpEditText=(EditText)findViewById(R.id.ip_send_edit_text);
        sendPortEditText=(EditText)findViewById(R.id.send_port_edit_text);

        runningTextView=(TextView) findViewById(R.id.running_text_view);
        ipTextView=(TextView) findViewById(R.id.ip_text_view);
        locationTextView=(TextView) findViewById(R.id.location_text_view);
//        providerTextView=(TextView) findViewById(R.id.provider_text_view);

        boardNameEditText=(EditText) findViewById(R.id.board_name_edit_text);
        sendAutoCheckBox=(CheckBox)findViewById(R.id.send_auto_checkbox);

//        receivedTextView=(TextView) findViewById(R.id.recieved_text_view);

        ipTextView.setText("My Ip: "+ Utils.getIPAddress(true));

        initConnectingButton();
        initSendManuallyButton();
    }



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        setRequestedOrientation (ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        initLocationModule();
        initUIElements();
        updateValuesFromBundle(savedInstanceState);
    }


    private void updateValuesFromBundle(Bundle savedInstanceState) {
        if (savedInstanceState == null) {
            return;
        }

        // Update the value of mRequestingLocationUpdates from the Bundle.
        if (savedInstanceState.keySet().contains(REQUESTING_LOCATION_UPDATES_KEY)) {
            mRequestingLocationUpdates = savedInstanceState.getBoolean(
                    REQUESTING_LOCATION_UPDATES_KEY);
        }

    }


    private void sendLocation()
    {
        JSONObject obj = new JSONObject();
        try {
            obj.put("long", longitude);
            obj.put("lat", latitude);
            obj.put("source", boardNameEditText.getText().toString());
        } catch (JSONException e) {
            e.printStackTrace();
            return;
        }
        if (mTcpClientSend != null) {
            mTcpClientSend.sendMessage(obj.toString());
        }
    }


//    private final LocationListener locationListener = new LocationListener() {
//
//
//        public void onLocationChanged(Location location) {
//            longitude = location.getLongitude();
//            latitude = location.getLatitude();
//            locationTextView.setText("("+String.valueOf(longitude)+","+String.valueOf(latitude)+")");
//            if(sendAutoCheckBox.isChecked())
//            {
//                sendLocation();
//            }
//        }
//
//        @Override
//        public void onStatusChanged(String provider, int status, Bundle extras) {
//            providerTextView.setText(provider+" "+String.valueOf(status));
//        }
//
//        @Override
//        public void onProviderEnabled(String provider) {
//
//        }
//
//        @Override
//        public void onProviderDisabled(String provider) {
//
//        }
//    };





    public class ConnectSendTask extends AsyncTask<String, String, TcpClient> {


        private void initTCPClient()
        {


            if (mTcpClientSend == null) {
                //we create a TCPClient object
                mTcpClientSend = new TcpClient(new TcpClient.OnMessageReceived() {
                    @Override
                    //here the messageReceived method is implemented
                    public void messageReceived(String from) {
                        Log.i("MainActivity", "messageFrom: " + from);
                    }
                });
            }


            mTcpClientSend.stopClient();
            mTcpClientSend.SERVER_IP = sendIpEditText.getText().toString();
            mTcpClientSend.SERVER_PORT = Integer.parseInt(sendPortEditText.getText().toString());
            mTcpClientSend.run();



        }


        @Override
        protected TcpClient doInBackground(String... message) {

            initTCPClient();
            return null;
        }

        @Override
        protected void onProgressUpdate(String... values) {
            super.onProgressUpdate(values);
            //response received from server
            Log.d("test", "response " + values[0]);
            //process server response here....


        }
    }


}















//    public class ConnectRecvTask extends AsyncTask<String, String, TcpClient> {
//
//
//        private void initTCPClient()
//        {
//
//            if (mTcpClientReceive == null) {
//                //we create a TCPClient object
//                mTcpClientReceive = new TcpClient(new TcpClient.OnMessageReceived() {
//                    @Override
//                    //here the messageReceived method is implemented
//                    public void messageReceived(String from) {
//                        Log.i("MainActivity", "messageFrom: " + from);
//
//                        JSONObject obj = new JSONObject();
//                        try {
//                            obj.put("long", longitude);
//                            obj.put("lat", latitude);
//                            obj.put("source", from);
//                            receivedTextView.setText("Received Send Location From : " + from);
//                            receivedTextView.setVisibility(View.VISIBLE);
//                        } catch (JSONException e) {
//                            e.printStackTrace();
//                            return;
//                        }
//                        if (mTcpClientSend != null) {
//                            mTcpClientSend.sendMessage(obj.toString());
//                        }
//                    }
//                });
//            }
//
//
//            mTcpClientReceive.stopClient();
//            mTcpClientReceive.SERVER_IP=receiveIpEditText.getText().toString();
//            mTcpClientReceive.SERVER_PORT=Integer.parseInt(receivePortEditText.getText().toString());
//            mTcpClientReceive.run();
//
//
//        }
//
//
//        @Override
//        protected TcpClient doInBackground(String... message) {
//
//            initTCPClient();
//            return null;
//        }
//
//        @Override
//        protected void onProgressUpdate(String... values) {
//            super.onProgressUpdate(values);
//            //response received from server
//            Log.d("test", "response " + values[0]);
//            //process server response here....
//
//
//        }
//    }