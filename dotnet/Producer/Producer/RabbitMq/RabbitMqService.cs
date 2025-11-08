using Microsoft.Extensions.Options;
using RabbitMQ.Client;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;


namespace Producer.RabbitMq
{
    public class RabbitMqService : IRabbitMqService
    {
        //private readonly RabbitMqConfiguration _configuration;
        //public RabbitMqService(IOptions<RabbitMqConfiguration> options)
        //    {
        //    _configuration = options.Value;
        //})
        public void SendMessage(object obj)
        {
            var message = JsonSerializer.Serialize(obj);
            SendMessage(message);
        }

        public void SendMessageAsync(string message)
        {
            // Не забудьте вынести значения "localhost" и "MyQueue"
            // в файл конфигурации
            //var factory = new ConnectionFactory() { HostName = "localhost" };
            var factory = new ConnectionFactory() 
            { 
                Uri = new Uri("amqps://jmnvgeqr:1FNeqMtZKcTKJSMqPRDVQUj9Oo1iBB-r@chimpanzee.rmq.cloudamqp.com/jmnvgeqr") 
            };
            using (var connection = factory.CreateConnectionAsync())
            using (var channel = connection.CreateModel())
            {
                channel.QueueDeclare(queue: "MyRabbit",
                               durable: false,
                               exclusive: false,
                               autoDelete: false,
                               arguments: null);

                var body = Encoding.UTF8.GetBytes(message);

                channel.BasicPublish(exchange: "",
                               routingKey: "MyRabbit",
                               basicProperties: null,
                               body: body);
            }
        }
    }
}
