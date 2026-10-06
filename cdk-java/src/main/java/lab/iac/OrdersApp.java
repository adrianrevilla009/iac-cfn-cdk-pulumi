package lab.iac;

import software.amazon.awscdk.App;
import software.amazon.awscdk.CfnOutput;
import software.amazon.awscdk.Duration;
import software.amazon.awscdk.RemovalPolicy;
import software.amazon.awscdk.Stack;
import software.amazon.awscdk.services.dynamodb.Attribute;
import software.amazon.awscdk.services.dynamodb.AttributeType;
import software.amazon.awscdk.services.dynamodb.BillingMode;
import software.amazon.awscdk.services.dynamodb.Table;
import software.amazon.awscdk.services.sqs.DeadLetterQueue;
import software.amazon.awscdk.services.sqs.Queue;

/** The shared Orders stack: same resources as cloudformation-stacks/orders-stack.yaml. */
public class OrdersApp {
    public static void main(String[] args) {
        App app = new App();
        Stack stack = new Stack(app, "OrdersStack");

        Queue dlq = Queue.Builder.create(stack, "OrdersDlq")
                .queueName("orders-dlq-dev")
                .retentionPeriod(Duration.days(14))
                .build();
        Queue queue = Queue.Builder.create(stack, "OrdersQueue")
                .queueName("orders-dev")
                .visibilityTimeout(Duration.seconds(30))
                .deadLetterQueue(DeadLetterQueue.builder().queue(dlq).maxReceiveCount(5).build())
                .build();
        Table table = Table.Builder.create(stack, "OrdersTable")
                .tableName("orders-dev")
                .billingMode(BillingMode.PAY_PER_REQUEST)
                .partitionKey(Attribute.builder().name("orderId").type(AttributeType.STRING).build())
                .removalPolicy(RemovalPolicy.DESTROY)
                .build();

        CfnOutput.Builder.create(stack, "QueueUrl").value(queue.getQueueUrl()).build();
        CfnOutput.Builder.create(stack, "TableName").value(table.getTableName()).build();
        app.synth();
    }
}
