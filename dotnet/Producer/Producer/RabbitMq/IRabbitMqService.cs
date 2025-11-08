using RabbitMQ.Client;

namespace Producer.RabbitMq
{
    public interface IRabbitMqService
    {
        void SendMessage(object obj);
        //void SendMessage(string message);
        void SendMessageAsync(string message);
        //Task DoOperationAsync(); // 
        //IConnection CreateChannel();
    }
}
