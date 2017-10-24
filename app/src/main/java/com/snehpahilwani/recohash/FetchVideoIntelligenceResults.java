package com.snehpahilwani.recohash;

/**
 * Created by Sneh P on 10/21/2017.
 */

import com.google.api.gax.rpc.OperationFuture;
import com.google.cloud.videointelligence.v1beta2.AnnotateVideoProgress;
import com.google.cloud.videointelligence.v1beta2.AnnotateVideoRequest;
import com.google.cloud.videointelligence.v1beta2.AnnotateVideoResponse;
import com.google.cloud.videointelligence.v1beta2.Entity;
import com.google.cloud.videointelligence.v1beta2.Feature;
import com.google.cloud.videointelligence.v1beta2.LabelAnnotation;
import com.google.cloud.videointelligence.v1beta2.LabelSegment;
import com.google.cloud.videointelligence.v1beta2.VideoAnnotationResults;
import com.google.cloud.videointelligence.v1beta2.VideoIntelligenceServiceClient;
import com.google.longrunning.Operation;
import java.util.List;

public class FetchVideoIntelligenceResults {

    /**
     * Demonstrates using the video intelligence client to detect labels in a video file.
     */
    public static void main(String[] args) throws Exception {
        // Instantiate a video intelligence client
        try (VideoIntelligenceServiceClient client = VideoIntelligenceServiceClient.create()) {
            // The Google Cloud Storage path to the video to annotate.
            String gcsUri = "gs://demomaker/cat.mp4";

            // Create an operation that will contain the response when the operation completes.
            AnnotateVideoRequest request = AnnotateVideoRequest.newBuilder()
                    .setInputUri(gcsUri)
                    .addFeatures(Feature.LABEL_DETECTION)
                    .build();

            OperationFuture<AnnotateVideoResponse, AnnotateVideoProgress, Operation> operation =
                    client.annotateVideoAsync(request);

            System.out.println("Waiting for operation to complete...");

            List<VideoAnnotationResults> results = operation.get().getAnnotationResultsList();
            if (results.isEmpty()) {
                System.out.println("No labels detected in " + gcsUri);
                return;
            }
            for (VideoAnnotationResults result : results) {
                System.out.println("Labels:");
                // get video segment label annotations
                for (LabelAnnotation annotation : result.getSegmentLabelAnnotationsList()) {
                    System.out
                            .println("Video label description : " + annotation.getEntity().getDescription());
                    // categories
                    for (Entity categoryEntity : annotation.getCategoryEntitiesList()) {
                        System.out.println("Label Category description : " + categoryEntity.getDescription());
                    }
                    // segments
                    for (LabelSegment segment : annotation.getSegmentsList()) {
                        double startTime = segment.getSegment().getStartTimeOffset().getSeconds()
                                + segment.getSegment().getStartTimeOffset().getNanos() / 1e9;
                        double endTime = segment.getSegment().getEndTimeOffset().getSeconds()
                                + segment.getSegment().getEndTimeOffset().getNanos() / 1e9;
                        System.out.printf("Segment location : %.3f:%.3f\n", startTime, endTime);
                        System.out.println("Confidence : " + segment.getConfidence());
                    }
                }
            }
        }
    }
}