package omar.mohamed.latif.gmail.com.smarthome;

import android.Manifest;
import android.content.Context;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
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

    private EditText ipEditText;

    private EditText portEditText;

    private TextView runningTextView;

    TcpClient mTcpClient;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        LocationManager lm = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            // TODO: Consider calling
            //    ActivityCompat#requestPermissions
            // here to request the missing permissions, and then overriding
            //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
            //                                          int[] grantResults)
            // to handle the case where the user grants the permission. See the documentation
            // for ActivityCompat#requestPermissions for more details.
            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.ACCESS_FINE_LOCATION},1);

        }
        lm.requestLocationUpdates(LocationManager.GPS_PROVIDER, 2000, 10, locationListener);

        ipEditText=(EditText)findViewById(R.id.ip_edit_text);
        portEditText=(EditText)findViewById(R.id.port_edit_text);
        runningTextView=(TextView) findViewById(R.id.running_text_view);
        Button sendLocationButton=(Button)findViewById(R.id.send_location_button);

        sendLocationButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (mTcpClient == null) {
                    //we create a TCPClient object
                    mTcpClient = new TcpClient(new TcpClient.OnMessageReceived() {
                        @Override
                        //here the messageReceived method is implemented
                        public void messageReceived(String message) {
                            Log.i("MainActivity","messageReceived: "+message);
                        }
                    });
                }
                mTcpClient.stopClient();
                TcpClient.SERVER_IP=ipEditText.getText().toString();
                TcpClient.SERVER_PORT=Integer.parseInt(portEditText.getText().toString());
                mTcpClient.run();
                runningTextView.setVisibility(View.VISIBLE);
            }
        });
    }


    private final LocationListener locationListener = new LocationListener() {


        public void onLocationChanged(Location location) {
           double longitude = location.getLongitude();
           double latitude = location.getLatitude();
            JSONObject obj = new JSONObject();
            try {
                obj.put("longitude", longitude);
                obj.put("latitude", latitude);
            } catch (JSONException e) {
                e.printStackTrace();
                return;
            }
           if(mTcpClient!=null)
           {
               mTcpClient.sendMessage(obj.toString());
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


}
