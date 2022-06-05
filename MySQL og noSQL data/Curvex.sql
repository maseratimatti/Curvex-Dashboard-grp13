Drop database if exists Curvex; #Sletter databasen hvis den allerede eksistere 
Create database Curvex; #Opretter databasen, ChargeHub_DA1_grp6
Use Curvex; #Benytter databasen ChargeHub_DA1_grp6

Drop table if exists Brugere; #Drop table benyttes til at slette alle tabellerne hvis de eksistere i forvejen

CREATE TABLE Brugere ( #Create table benyttes til at oprette en ny tabel, i dette tilfælde "Bruger" 
    b_id int NOT NULL AUTO_INCREMENT, #int benyttes til at sikre det bliver et tal. Not null bruges til det skal have en værdi. Auto_increment benyttes til at tabellen automatisk giver b_id et tal startende fra 1
    b_fornavn varchar(30) NOT NULL, #varchar benyttes til at definere at inputtet kan være tal og tegn, med et maks på 30 tegn. Not null bruges igen til at sige der skal være et input 
    b_efternavn varchar(100) NOT NULL,
    b_password varchar(100) NOT NULL,
    b_telefon int(8) NOT NULL,
    b_email varchar(100) NOT NULL,
    PRIMARY KEY (b_id) #Primary key benyttes til at definere den primære nøgle i tabellen, som i dette tilfælde er b_id
);

INSERT INTO Brugere #Insert into benyttes til at sætte data ind i tabellen Bruger
	(b_fornavn, b_efternavn, b_password, b_telefon, b_email) #Kolonnerne der skal værdi i skrives i parentes, adskilt med komma
VALUES 
	('Solvej', 'Andersen', 'Hejhej1234', '20852013', 'solvej@gmail.com'), #Tegnene ' ' benyttes til at sætte værdierne ind i kolonnerne, igen adskilt med komma
	('Frank', 'Christensen', 'Farvel1234', '30456912', 'Frankc@hotmail.com'),
    ('Alice', 'Vestergaard', 'Abcd1234', '50898740', 'alicevest@gmail.com'),
    ('Charlotte', 'Jensen', 'Abcdefg', '40508920', 'charlottejensen@hotmail.com'),
    ('Karsten', 'Jørgen', 'KJs923', '4050920', 'karstenmanden@hotmail.com'),
	('Jakob', 'Lundshøj', ' LLj24fa', '90293017', 'jakoblundshoej@gmail.com'),
    ('Rebecca', 'Terki', 'KJKJlk021', '30823421', 'rebterki@gmail.com'),
    ('Jonas', 'Hansen', ' MCmck200', '20901919', 'j.hansen@hotmail.com'),
    ('Karsten', 'Jonsons', 'Hejheeej23', '50981780', 'karsten.j@gmail.com'),
    ('Emil', 'Tange', 'Lisa12315', '40591120', 'emil.tange@hotmail.com');
    