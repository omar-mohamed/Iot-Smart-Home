package omar.mohamed.latif.gmail.com.smarthome;

import android.Manifest;
import android.content.Context;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;

public class MainActivity extends AppCompatActivity {

    private EditText receiveIpEditText;
    private EditText receivePortEditText;

    private EditText sendIpEditText;
    private EditText sendPortEditText;

    private TextView runningTextView;

    private TextView ipTextView;

    private TextView receivedTextView;

    private TcpClient mTcpClientReceive;
    private TcpClient mTcpClientSend;


    private double longitude=0;
    private double latitude=0;

    private void initLocationModule()
    {
        LocationManager lm = (LocationManager) getSystemService(Context.LOCATION_SERVICE);

        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.ACCESS_FINE_LOCATION},1);

        }
        lm.requestLocationUpdates(LocationManager.GPS_PROVIDER, 5000, 2, locationListener);

    }



    private void initListeningButton()
    {
        Button ListeningButton=(Button)findViewById(R.id.start_listening_button);

        ListeningButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                ipTextView.setText("My Ip: " + Utils.getIPAddress(true));
                runningTextView.setVisibility(View.VISIBLE);
                new ConnectRecvTask().executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);
                new ConnectSendTask().executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);

            }
        });
    }



    private void initUIElements()
    {
        receiveIpEditText=(EditText)findViewById(R.id.ip_recieve_edit_text);
        receivePortEditText=(EditText)findViewById(R.id.receive_port_edit_text);

        sendIpEditText=(EditText)findViewById(R.id.ip_send_edit_text);
        sendPortEditText=(EditText)findViewById(R.id.send_port_edit_text);

        runningTextView=(TextView) findViewById(R.id.running_text_view);
        ipTextView=(TextView) findViewById(R.id.ip_text_view);
        receivedTextView=(TextView) findViewById(R.id.recieved_text_view);

        ipTextView.setText("My Ip: "+ Utils.getIPAddress(true));

        initListeningButton();

    }



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        initLocationModule();
        initUIElements();
    }


    private final LocationListener locationListener = new LocationListener() {


        public void onLocationChanged(Location location) {
            longitude = location.getLongitude();
            latitude = location.getLatitude();

            JSONObject obj = new JSONObject();
            try {
                obj.put("long", longitude);
                obj.put("lat", latitude);
                obj.put("source", "Board 1");
            } catch (JSONException e) {
                e.printStackTrace();
                return;
            }
            if (mTcpClientSend != null) {
                mTcpClientSend.sendMessage(obj.toString());
            }
        }

        @Override
        public void onStatusChanged(String provider, int status, Bundle extras) {

        }

        @Override
        public void onProviderEnabled(String provider) {

        }

        @Override
        public void onProviderDisabled(String provider) {

        }
    };




    public class ConnectRecvTask extends AsyncTask<String, String, TcpClient> {


        private void initTCPClient()
        {

            if (mTcpClientReceive == null) {
                //we create a TCPClient object
                mTcpClientReceive = new TcpClient(new TcpClient.OnMessageReceived() {
                    @Override
                    //here the messageReceived method is implemented
                    public void messageReceived(String from) {
                        Log.i("MainActivity", "messageFrom: " + from);

                        JSONObject obj = new JSONObject();
                        try {
                            obj.put("long", longitude);
                            obj.put("lat", latitude);
                            obj.put("source", from);
                            receivedTextView.setText("Received Send Location From : " + from);
                            receivedTextView.setVisibility(View.VISIBLE);
                        } catch (JSONException e) {
                            e.printStackTrace();
                            return;
                        }
                        if (mTcpClientSend != null) {
                            mTcpClientSend.sendMessage(obj.toString());
                        }
                    }
                });
            }


            mTcpClientReceive.stopClient();
            mTcpClientReceive.SERVER_IP=receiveIpEditText.getText().toString();
            mTcpClientReceive.SERVER_PORT=Integer.parseInt(receivePortEditText.getText().toString());
            mTcpClientReceive.run();


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
