package com.snehpahilwani.recohash;

/**
 * Created by Sneh P on 10/21/2017.
 */


import android.content.ContentUris;
import android.content.Context;
import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.provider.DocumentsContract;
import android.provider.MediaStore;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import java.io.File;
import java.net.URISyntaxException;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Button uploadButton = (Button)findViewById(R.id.btn_upload);

        final Intent fileChooseIntent = new Intent()
                .setType("*/*")
                .setAction(Intent.ACTION_GET_CONTENT);
        uploadButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivityForResult(Intent.createChooser(fileChooseIntent, "Select a media file"), 1);
            }
        });
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        final EditText editTextDisplay = (EditText) findViewById(R.id.editTextDisplay);
        if(requestCode==1 && resultCode==RESULT_OK) {
            Uri selectedFile = data.getData(); //The uri with the location of the file
           File myFile = new File(selectedFile.getPath());

            Log.println(Log.DEBUG,"print URL",selectedFile.getPath());
            editTextDisplay.setText(myFile.toString());
        }
    }


}
