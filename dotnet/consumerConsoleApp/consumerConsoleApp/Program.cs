using consumerConsoleApp;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;
using System.Diagnostics;
using System.Text;



string host = HostnameClass.host;

var factory = new ConnectionFactory() { Uri = new Uri(host) };
using var connection = await factory.CreateConnectionAsync();
using var channel = await connection.CreateChannelAsync();

await channel.QueueDeclareAsync(queue: "dotnetRabbit", 
    durable: false, 
    exclusive: false, 
    autoDelete: false,
    arguments: null);

Debug.WriteLine(" [*] Waiting for messages.");

var consumer = new AsyncEventingBasicConsumer(channel);
consumer.ReceivedAsync += (model, ea) =>
{
    var body = ea.Body.ToArray();
    var message = Encoding.UTF8.GetString(body);
    Debug.WriteLine($" [x] Received {message}");
    return Task.CompletedTask;
};

await channel.BasicConsumeAsync("dotnetRabbit", 
                                autoAck: true, 
                                consumer: consumer);

//Debug.WriteLine(" Press [enter] to exit.");
//Console.ReadLine();



