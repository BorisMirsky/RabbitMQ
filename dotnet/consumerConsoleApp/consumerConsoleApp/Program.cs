using RabbitMQ.Client;
using RabbitMQ.Client.Events;
using System;
using System.Text;

static async void Main(string[] args)
{

    string host = "amqps://jmnvgeqr:1FNeqMtZKcTKJSMqPRDVQUj9Oo1iBB-r@chimpanzee.rmq.cloudamqp.com:5671/jmnvgeqr";
    var factory = new ConnectionFactory() {Uri = new Uri(host) };
    using var connection = await factory.CreateConnectionAsync();
    using var channel = await connection.CreateChannelAsync();
    await channel.QueueDeclareAsync(queue: "dotnetRabbit",
                                     durable: false,
                                     exclusive: false,
                                     autoDelete: false,
                                     arguments: null);

    var consumer = new EventingBasicConsumer(channel);
    consumer.Received += (model, ea) =>
        {
            var body = ea.Body.ToArray();
            var message = Encoding.UTF8.GetString(body);
            Console.WriteLine(" [x] Received {0}", message);
        };
    channel.BasicConsumeAsync(queue: "MyQueue",
                             autoAck: true,
                             consumer: consumer);

    Console.WriteLine(" Press [enter] to exit.");
    Console.ReadLine();
    }
}