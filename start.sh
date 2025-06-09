#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if settings.ini already exists
if [ -f "settings.ini" ]; then
    print_warning "settings.ini already exists!"
    read -p "Do you want to overwrite it? (y/N): " overwrite
    if [[ ! $overwrite =~ ^[Yy]$ ]]; then
        print_message "Using existing settings.ini"
    else
        rm settings.ini
    fi
fi

# Function to get input with default value
get_input() {
    local prompt="$1"
    local default="$2"
    local value
    
    if [ -n "$default" ]; then
        read -p "$prompt [$default]: " value
        echo "${value:-$default}"
    else
        while true; do
            read -p "$prompt: " value
            if [ -n "$value" ]; then
                echo "$value"
                break
            fi
            print_error "This field cannot be empty!"
        done
    fi
}

# Get Telegram Bot Token
print_message "Let's configure your bot!"
print_message "You can get your Telegram Bot Token from @BotFather"
telegram_token=$(get_input "Enter your Telegram Bot Token")

# Get LLM API settings
print_message "\nNow let's configure the LLM API settings"
llm_url=$(get_input "Enter LLM API URL" "http://51.250.75.212:11434/api/generate")
llm_model=$(get_input "Enter model name" "llama2:13b-text")

# Get logging settings
print_message "\nConfiguring logging settings"
log_level=$(get_input "Enter logging level (DEBUG/INFO/WARNING/ERROR/CRITICAL)" "INFO")
log_file=$(get_input "Enter log file path" "bot.log")

# Create settings.ini
cat > settings.ini << EOL
# settings.ini
[telegram]
token = ${telegram_token}

[llm]
url = ${llm_url}
model = ${llm_model}

[logging]
level = ${log_level}
file = ${log_file}
EOL

print_message "\nsettings.ini has been created successfully!"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed! Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed! Please install Docker Compose first."
    exit 1
fi

# Build and start the container
print_message "\nBuilding and starting the container..."
print_message "This might take a few minutes..."

# Build the image
if docker build -t kristybot .; then
    print_message "Docker image built successfully!"
else
    print_error "Failed to build Docker image!"
    exit 1
fi

# Start the container
if docker-compose up -d; then
    print_message "Container started successfully!"
    print_message "You can check the logs with: docker-compose logs -f"
else
    print_error "Failed to start container!"
    exit 1
fi

print_message "\nSetup completed! Your bot should be running now."
print_message "Use the following commands to manage your bot:"
echo -e "  ${YELLOW}docker-compose logs -f${NC}  - View logs"
echo -e "  ${YELLOW}docker-compose down${NC}    - Stop the bot"
echo -e "  ${YELLOW}docker-compose up -d${NC}   - Start the bot"
echo -e "  ${YELLOW}docker-compose restart${NC} - Restart the bot" 