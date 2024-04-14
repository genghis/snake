import aws_cdk as core
import aws_cdk.assertions as assertions

from battlesnake.battlesnake_stack import BattlesnakeStack

# example tests. To run these tests, uncomment this file along with the example
# resource in battlesnake/battlesnake_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = BattlesnakeStack(app, "battlesnake")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
