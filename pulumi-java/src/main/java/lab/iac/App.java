package lab.iac;

import com.pulumi.Pulumi;
import com.pulumi.aws.dynamodb.Table;
import com.pulumi.aws.dynamodb.TableArgs;
import com.pulumi.aws.dynamodb.inputs.TableAttributeArgs;
import com.pulumi.aws.sqs.Queue;
import com.pulumi.aws.sqs.QueueArgs;

/** The shared Orders stack: same resources as cloudformation-stacks/orders-stack.yaml. */
public class App {
    public static void main(String[] args) {
        Pulumi.run(ctx -> {
            var dlq = new Queue("orders-dlq", QueueArgs.builder()
                    .name("orders-dlq-dev")
                    .messageRetentionSeconds(1209600)
                    .build());
            var queue = new Queue("orders", QueueArgs.builder()
                    .name("orders-dev")
                    .visibilityTimeoutSeconds(30)
                    .redrivePolicy(dlq.arn().applyValue(arn ->
                            "{\"deadLetterTargetArn\":\"" + arn + "\",\"maxReceiveCount\":5}"))
                    .build());
            var table = new Table("orders", TableArgs.builder()
                    .name("orders-dev")
                    .billingMode("PAY_PER_REQUEST")
                    .hashKey("orderId")
                    .attributes(TableAttributeArgs.builder().name("orderId").type("S").build())
                    .build());

            ctx.export("queueUrl", queue.url());
            ctx.export("tableName", table.name());
        });
    }
}
