// BankingSystem.java
// Java Console Application for basic banking operations

import java.util.*;

class Account {
    private static int nextId = 1;
    private int accountId;
    private String holderName;
    private double balance;

    public Account(String holderName, double initialDeposit) {
        this.accountId = nextId++;
        this.holderName = holderName;
        this.balance = initialDeposit;
    }

    public int getAccountId() {
        return accountId;
    }

    public String getHolderName() {
        return holderName;
    }

    public double getBalance() {
        return balance;
    }

    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
        }
    }

    public boolean withdraw(double amount) {
        if (amount > 0 && amount <= balance) {
            balance -= amount;
            return true;
        }
        return false;
    }

    public void displayDetails() {
        System.out.println("Account ID: " + accountId);
        System.out.println("Holder Name: " + holderName);
        System.out.println("Balance: Rs. " + balance);
    }
}

public class BankingSystem {
    private static List<Account> accounts = new ArrayList<>();
    private static Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        while (true) {
            System.out.println("\n=== Banking System Menu ===");
            System.out.println("1. Create New Account");
            System.out.println("2. Deposit");
            System.out.println("3. Withdraw");
            System.out.println("4. Check Balance");
            System.out.println("5. Display Account Details");
            System.out.println("6. Exit");
            System.out.print("Enter your choice: ");
            int choice = getIntInput();

            switch (choice) {
                case 1:
                    createAccount();
                    break;
                case 2:
                    deposit();
                    break;
                case 3:
                    withdraw();
                    break;
                case 4:
                    checkBalance();
                    break;
                case 5:
                    displayAccountDetails();
                    break;
                case 6:
                    System.out.println("Thank you for using the Banking System!");
                    return;
                default:
                    System.out.println("Invalid choice. Please try again.");
            }
        }
    }

    private static void createAccount() {
        System.out.print("Enter account holder name: ");
        String name = scanner.nextLine();
        System.out.print("Enter initial deposit amount: ");
        double deposit = getDoubleInput();
        Account acc = new Account(name, deposit);
        accounts.add(acc);
        System.out.println("Account created successfully! Account ID: " + acc.getAccountId());
    }

    private static Account findAccount() {
        System.out.print("Enter account ID: ");
        int id = getIntInput();
        for (Account acc : accounts) {
            if (acc.getAccountId() == id) {
                return acc;
            }
        }
        System.out.println("Account not found.");
        return null;
    }

    private static void deposit() {
        Account acc = findAccount();
        if (acc != null) {
            System.out.print("Enter deposit amount: ");
            double amount = getDoubleInput();
            acc.deposit(amount);
            System.out.println("Deposit successful. New balance: Rs. " + acc.getBalance());
        }
    }

    private static void withdraw() {
        Account acc = findAccount();
        if (acc != null) {
            System.out.print("Enter withdrawal amount: ");
            double amount = getDoubleInput();
            if (acc.withdraw(amount)) {
                System.out.println("Withdrawal successful. New balance: Rs. " + acc.getBalance());
            } else {
                System.out.println("Insufficient balance or invalid amount.");
            }
        }
    }

    private static void checkBalance() {
        Account acc = findAccount();
        if (acc != null) {
            System.out.println("Current balance: Rs. " + acc.getBalance());
        }
    }

    private static void displayAccountDetails() {
        Account acc = findAccount();
        if (acc != null) {
            acc.displayDetails();
        }
    }

    private static int getIntInput() {
        while (true) {
            try {
                return Integer.parseInt(scanner.nextLine());
            } catch (NumberFormatException e) {
                System.out.print("Invalid input. Please enter a number: ");
            }
        }
    }

    private static double getDoubleInput() {
        while (true) {
            try {
                return Double.parseDouble(scanner.nextLine());
            } catch (NumberFormatException e) {
                System.out.print("Invalid input. Please enter a valid amount: ");
            }
        }
    }
}
