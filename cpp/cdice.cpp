#include <iostream>
#include <string>
#include <random>

#define GT 0
#define GE 1
#define LT 2
#define LE 3

using namespace std;

int calc(string calc_str);
bool chknum(string str, int start = 0, int end = -1);
int dice(string dice_str, int indicator = -1, int thresh = -1);
int totcalc(string totcalc_str);


int main(int argc, char **argv)
{
    std::srand(time(NULL));
    char inp[10];

    if (argc > 1)
        for (int i = 1; i < argc; ++i)
            totcalc(string(argv[i]));
    else
    {
        while (cin >> inp)
            totcalc(string(inp));
        return 0;
    }
}

int totcalc(string totcalc_str)
{
    if (calc(totcalc_str) == 0)
        return 0;
    cout << ">> " << totcalc_str 
        <<"\n\tCannot Recognize the input" << endl;
    return -1;
}

int calc(string calc_str)
{
    string dice_str;
    int indicator_pos = -1;
    int indicator_len = 2;
    int thresh = -1;
    int indicator = -1;

    for (int i = 0; i < (int)calc_str.length(); ++i)
        calc_str[i] = tolower(calc_str[i]);

    if ((indicator_pos = calc_str.find("gt")) > 0)
        indicator = GT;
    else if ((indicator_pos = calc_str.find("ge")) > 0)
        indicator = GE;
    else if ((indicator_pos = calc_str.find("lt")) > 0)
        indicator = LT;
    else if ((indicator_pos = calc_str.find("le")) > 0)
        indicator = LE;
    else if ((indicator_pos = calc_str.find(">=")) > 0)
        indicator = GE;
    else if ((indicator_pos = calc_str.find("<=")) > 0)
        indicator = LE;
    else 
    {
        indicator_len = 1;
        if ((indicator_pos = calc_str.find("l")) > 0)
            indicator = LT;
        else if ((indicator_pos = calc_str.find("g")) > 0)
            indicator = GT;
        else if ((indicator_pos = calc_str.find(">")) > 0)
            indicator = GT;
        else if ((indicator_pos = calc_str.find("<")) > 0)
            indicator = LT;
        else
        {
            indicator = -1;
            indicator_len = 0;
            indicator_pos = -1;
            dice_str = calc_str;
        }
    }
    if (indicator != -1)
    {
        dice_str = calc_str.substr(0, indicator_pos);
        if (chknum(calc_str, indicator_pos+indicator_len))
            thresh = stoi(calc_str.substr(indicator_pos+indicator_len));
        else
            thresh = -1;
    }

    if (dice(dice_str, indicator, thresh))
        return -1;
    else 
        return 0;
}

bool chknum(string str, int start, int end)
{
    bool flag = true;
    if (end == -1)
        end = (int)str.length();

    for (int i = start; i < end; ++i)
        flag &= isdigit(str[i]);
    return start < end ? flag && stoi(str.substr(start, end)) > 0 : false;
}

int dice(string dice_str, int indicator, int thresh)
{
    int dpos, dice_count, dice_faces;
    int tempres;
    int rescount = 0;
    string str = string(dice_str);

    dpos = str.find('d');
    if (dpos == -1)
        dpos = str.find('D');

    switch (dpos)
    {
        case -1:
            if ((int) str.length() > 0)
            {
                if (chknum(str))
                    dice_count = stoi(str);
                else
                    return -1;
            }
            else
                dice_count = 1;
            dice_faces = 6;
            break;
        case 0:
            if (dpos == (int)str.length() - 1)
                dice_faces = 1;
            else if (chknum(str, dpos+1))
                dice_faces = stoi(str.substr(dpos+1));
            else
                return -1;
            dice_count = 1;
            break;
        default:
            if (chknum(str, 0, dpos))
                dice_count = stoi(str.substr(0, dpos));
            else
                return -1;

            if ((int) str.length() -1 == dpos)
            {
                if (chknum(str, 0, dpos))
                    dice_count = stoi(str.substr(0, dpos));
                else
                    return -1;
                dice_faces = 6;
            }
            else if (chknum(str, dpos+1))
                dice_faces = stoi(str.substr(dpos+1));
            else
                return -1;
    }
    cout << ">> " << dice_count << "D" << dice_faces;
    
    if (thresh > 0)
        switch (indicator)
        {
            case GT:
                cout << ">" << thresh << endl;
                break;
            case GE:
                cout << ">=" << thresh << endl;
                break;
            case LT:
                cout << "<" << thresh << endl;
                break;
            case LE:
                cout << "<=" << thresh << endl;
        }

    cout << "\tResult: ";
    for (int i = 0; i < dice_count; ++i)
    {
        tempres = rand() % dice_faces + 1;
        switch (indicator)
        {
            case GT:
                rescount += (int) (tempres > thresh);
                break;
            case GE:
                rescount += (int) (tempres >= thresh);
                break;
            case LT:
                rescount += (int) (tempres < thresh);
                break;
            case LE:
                rescount += (int) (tempres <= thresh);
                break;
        }
        cout << tempres << ' ';
    }
    cout << endl;
    if (thresh != -1)
    {
        if (dice_count == 1)
            cout << '\t' << (rescount?"Success!":"Failed") << endl;
        else
            cout << "\tSuccess: " << rescount << endl;
    }

    return 0;
}
