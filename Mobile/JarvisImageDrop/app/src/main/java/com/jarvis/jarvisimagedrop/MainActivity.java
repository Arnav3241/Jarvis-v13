package com.jarvis.jarvisimagedrop;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.StorageReference;
import java.util.Objects;

public class MainActivity extends AppCompatActivity {

    private ImageView imageView;
    private TextView urlShowTV;
    public Uri imageUri;
    private StorageReference storageReference;
    FirebaseDatabase db;
    DatabaseReference reference;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        imageView = findViewById(R.id.imageView);
        urlShowTV = findViewById(R.id.urlShowTextView);


        // Get the intent that started this activity
        Intent receivedIntent = getIntent();
        if (receivedIntent != null && receivedIntent.getAction() != null) {
            if (receivedIntent.getAction().equals(Intent.ACTION_SEND) && receivedIntent.getType() != null) {
                if (receivedIntent.getType().startsWith("image/")) {
                    // Get the shared image URI
                    imageUri = (Uri) receivedIntent.getParcelableExtra(Intent.EXTRA_STREAM);

                    // Display the shared image in an ImageView
                    ImageView imageView = findViewById(R.id.imageView);
                    imageView.setImageURI(imageUri);

//                    String downloadUrl = (new UploadImage_(this, imageUri, urlShowTV)).uploadImage();

                     uploadImageToFirebaseStorage();
                }
            }
        }
    }

    private void uploadImageToFirebaseStorage() {

        if (imageUri != null) {

            UploadImage_ uploadImage = new UploadImage_(this, imageUri, urlShowTV);
            uploadImage.uploadImage(new UploadImage_.UploadCallback() {
                @Override
                public void onSuccess(String downloadUrl) {
                    // Image uploaded successfully
                    db = FirebaseDatabase.getInstance("https://jarvisfiledrop-default-rtdb.asia-southeast1.firebasedatabase.app/");
                    reference = db.getReference("Link");
                    reference.setValue(downloadUrl);
                    urlShowTV.setText(downloadUrl);
//                    reference.child("Link").setValue(downloadUrl).addOnCompleteListener(new OnCompleteListener<Void>() {
//                        @Override
//                        public void onComplete(@NonNull Task<Void> task) {
//                            Toast.makeText(MainActivity.this, "Successfully Updated Realtime DB", Toast.LENGTH_SHORT).show();
//                            urlShowTV.setText(downloadUrl);
//                            // Close the app after updating the Realtime Database
//                            finish();
//                        }
//                    });
                    Toast.makeText(MainActivity.this, "Image uploaded to Firebase Storage", Toast.LENGTH_SHORT).show();
                    finish();
                }

                @Override
                public void onFailure(String errorMessage) {
                    // Handle image upload failure
                    Toast.makeText(MainActivity.this, errorMessage, Toast.LENGTH_SHORT).show();
                }
            });
        }
    }
}